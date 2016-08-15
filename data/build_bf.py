#!/usr/bin/env python
# pylint: disable=missing-docstring,invalid-name,redefined-outer-name
import csv
import json

from bs4 import BeautifulSoup
from pybloom import ScalableBloomFilter
import requests

# Settings
INITIAL_CAPACITY = 2000000
ERROR_RATE = 0.001

# Systems
LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'
RXNORM = 'http://www.nlm.nih.gov/research/umls/rxnorm'
ICD10 = 'http://hl7.org/fhir/sid/icd-10'

# SOURCES
LOINC_PATH = './loinc/loinc.csv'
SNOMED_PATH = './snomed/SnomedCT_RF2Release_INT_20160131/Full/Terminology/sct2_Concept_Full_INT_20160131.txt'
RXNORM_PATH = './rxnorm/rrf/RXNCONSO.RRF'
RXNORM_DEPRECATED_PATH = './rxnorm/rrf/RXNCUI.RRF'
ICD10_PATH = './icd10/icd10cm_tabular_2017.xml'


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


def import_fhir(bf):
    value_set_definition_urls = [
        'http://hl7.org/fhir/valuesets.json',
        'http://hl7.org/fhir/v2-tables.json',
        'http://hl7.org/fhir/v3-codesystems.json',
    ]

    fhir_systems = []

    def get_codes_from_concept(code_system):
        codes = []

        if 'code' in code_system:
            codes.append(code_system['code'])

        concepts = code_system.get('concept', [])
        for concept in concepts:
            codes += get_codes_from_concept(concept)

        return codes

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

    with open('./fhir/systems.json', 'w') as handle:
        json.dump(fhir_systems, handle)


try:
    # If the bloom filter already exists, we're probably just appending to it
    with open('./codes.bf', 'rb') as handle:
        bf = ScalableBloomFilter.fromfile(handle)
except FileNotFoundError:
    # If it doesn't, we need to make one
    bf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH,
                             initial_capacity=INITIAL_CAPACITY,
                             error_rate=ERROR_RATE)

import_loinc(bf)
import_snomed(bf)
import_rxnorm(bf)
import_icd10(bf)
import_fhir(bf)

if __name__ == '__main__':
    with open('./codes.bf', 'wb') as handle:
        bf.tofile(handle)
