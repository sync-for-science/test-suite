#!/usr/bin/env python
# pylint: disable=missing-docstring,invalid-name,redefined-outer-name
import csv
import json
from os import path
import re

from bs4 import BeautifulSoup
from pybloom import ScalableBloomFilter
import requests

# Systems
from testsuite.systems import (
    LOINC,
    SNOMED,
    RXNORM,
    ICD9,
    ICD10,
    CPT,
    CVX,
)

# Settings
INITIAL_CAPACITY = 2000000
ERROR_RATE = 0.001
DATA_DIR = path.dirname(__file__)

# SOURCES
LOINC_PATH = path.join(DATA_DIR, 'loinc', 'loinc.csv')
SNOMED_PATH = path.join(DATA_DIR, 'snomed', 'SnomedCT_RF2Release_INT_20160131', 'Full', 'Terminology', 'sct2_Concept_Full_INT_20160131.txt')
RXNORM_PATH = path.join(DATA_DIR, 'rxnorm', 'rrf', 'RXNCONSO.RRF')
RXNORM_DEPRECATED_PATH = path.join(DATA_DIR, 'rxnorm', 'rrf', 'RXNCUI.RRF')
ICD9_PATH = path.join(DATA_DIR, 'icd9', 'CMS32_DESC_LONG_DX.txt')
ICD10_PATH = path.join(DATA_DIR, 'icd10', 'icd10cm_tabular_2017.xml')
CPT_PATH = path.join(DATA_DIR, 'cpt', 'MRCONSO.RRF')
CVX_PATH = path.join(DATA_DIR, 'cvx', 'cvx.txt')
ARGO_VITAL_SIGNS_PATH = path.join(DATA_DIR, 'fhir', 'argo-vital-signs.json')
ARGO_EXTENSIONS_PATH = path.join(DATA_DIR, 'fhir', 'argo-extension-codes.json')

# DESTINATIONS
ARGO_SYSTEMS_PATH = path.join(DATA_DIR, 'fhir', 'argo.json')
DAF_SYSTEMS_PATH = path.join(DATA_DIR, 'fhir', 'daf.json')
FHIR_SYSTEMS_PATH = path.join(DATA_DIR, 'fhir', 'systems.json')
BF_PATH = path.join(DATA_DIR, 'codes.bf')


def import_loinc(bf):
    with open(LOINC_PATH) as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            bf.add(LOINC + '|' + row['LOINC_NUM'])


def import_snomed(bf):
    with open(SNOMED_PATH) as handle:
        reader = csv.DictReader(handle, delimiter='\t')

        for row in reader:
            bf.add(SNOMED + '|' + row['id'])


def import_rxnorm(bf):
    unique = set()

    fieldnames = [
        'RXCUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'RXAUI',
        'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL',
        'SUPPRESS', 'CVF',
    ]

    with open(RXNORM_PATH) as handle:
        reader = csv.DictReader(handle, delimiter='|', fieldnames=fieldnames)
        unique.update([row['RXCUI'] for row in reader])

    fieldnames = [
        'RXCUI1', 'VSAB_START', 'VSAB_END', 'Cardinality', 'RXCUI2',
    ]

    with open(RXNORM_DEPRECATED_PATH) as handle:
        reader = csv.DictReader(handle, delimiter='|', fieldnames=fieldnames)
        unique.update([row['RXCUI1'] for row in reader])

    for code in unique:
        bf.add(RXNORM + '|' + code)


def import_icd10(bf):
    with open(ICD10_PATH) as handle:
        soup = BeautifulSoup(handle, 'html.parser')

    tags = soup.select('section name')
    unique = set([tag.string for tag in tags])

    for code in unique:
        bf.add(ICD10 + '|' + code)


def import_icd9(bf):
    with open(ICD9_PATH, encoding='cp1252') as handle:
        for line in handle.readlines():
            code, desc = re.split(r'\s+', line, maxsplit=1)
            bf.add(ICD9 + '|' + code)
            # Splice a "." into the code at position 3
            dot_code = '.'.join((code[:3], code[3:]))
            bf.add(ICD9 + '|' + dot_code)


def import_cpt(bf):
    with open(CPT_PATH) as handle:
        reader = csv.DictReader(handle, delimiter='|')

        rows = list(reader)
        unique = set([row['CODE'] for row in rows])

        for code in unique:
            bf.add(CPT + '|' + code)


def get_codes_from_concept(code_system):
    codes = []

    if 'code' in code_system:
        codes.append(code_system['code'])

    concepts = code_system.get('concept', [])
    for concept in concepts:
        codes += get_codes_from_concept(concept)

    return codes


def import_fhir(bf):
    value_set_definition_urls = [
        'http://hl7.org/fhir/valuesets.json',
        'http://hl7.org/fhir/v2-tables.json',
        'http://hl7.org/fhir/v3-codesystems.json',
    ]

    fhir_systems = []

    def get_value_sets(url):
        res = requests.get(url)
        bundle = res.json()

        return [entry['resource'] for entry in bundle['entry']
                if 'codeSystem' in entry['resource']]

    for value_set_url in value_set_definition_urls:
        value_sets = get_value_sets(value_set_url)

        for value_set in value_sets:
            url = value_set['codeSystem']['system']
            codes = get_codes_from_concept(value_set['codeSystem'])

            for code in codes:
                bf.add(url + '|' + code)

            fhir_systems.append(url)

    with open(FHIR_SYSTEMS_PATH, 'w') as handle:
        json.dump(fhir_systems, handle)


def import_daf(bf):
    value_set_definition_urls = [
        'http://hl7.org/fhir/daf/valueset-daf-observation-ccdasmokingstatus.json',
        'http://hl7.org/fhir/daf/valueset-daf-observation-CCDAVitalSignResult.json',
        'http://hl7.org/fhir/daf/valueset-daf-cvx.json',
        'http://hl7.org/fhir/DSTU2/daf/valueset-daf-problem.json',
    ]

    daf_systems = []

    def get_value_set(url):
        res = requests.get(url)
        return res.json()

    for value_set_url in value_set_definition_urls:
        value_set = get_value_set(value_set_url)
        url = value_set['url']

        for include in value_set['compose']['include']:
            codes = get_codes_from_concept(include)

            for code in codes:
                bf.add(url + '|' + code)

        daf_systems.append(url)

    with open(DAF_SYSTEMS_PATH, 'w') as handle:
        json.dump(daf_systems, handle)


def import_argo(bf):
    paths = ARGO_VITAL_SIGNS_PATH, ARGO_EXTENSIONS_PATH

    argo_systems = []

    def get_value_set(path):
        with open(path) as handle:
            return json.load(handle)

    for path in paths:
        value_set = get_value_set(path)
        url = value_set['url']

        for include in value_set['compose']['include']:
            codes = get_codes_from_concept(include)

            for code in codes:
                bf.add(url + '|' + code)

        argo_systems.append(url)

    with open(ARGO_SYSTEMS_PATH, 'w') as handle:
        json.dump(argo_systems, handle)


def import_cvx(bf):
    fieldnames = [
        'cvx code',
        'short description',
        'full vaccines name',
        'notes',
        'vaccine status',
        'nonvaccine',
        'last updated date',
    ]
    with open(CVX_PATH, encoding='utf-16') as handle:
        reader = csv.DictReader(handle, delimiter='|', fieldnames=fieldnames)

        for row in reader:
            bf.add(CVX + '|' + row['cvx code'].strip())


try:
    # If the bloom filter already exists, we're probably just appending to it
    with open(BF_PATH, 'rb') as handle:
        bf = ScalableBloomFilter.fromfile(handle)
except FileNotFoundError:
    # If it doesn't, we need to make one
    bf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH,
                             initial_capacity=INITIAL_CAPACITY,
                             error_rate=ERROR_RATE)

import_loinc(bf)
import_snomed(bf)
import_rxnorm(bf)
import_icd9(bf)
import_icd10(bf)
import_cpt(bf)
import_fhir(bf)
import_daf(bf)
import_argo(bf)
import_cvx(bf)

if __name__ == '__main__':
    with open(BF_PATH, 'wb') as handle:
        bf.tofile(handle)
