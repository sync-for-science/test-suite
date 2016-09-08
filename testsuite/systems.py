""" Validate provided codes.
"""
import json

from pybloom import ScalableBloomFilter


LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'
RXNORM = 'http://www.nlm.nih.gov/research/umls/rxnorm'
ICD10 = 'http://hl7.org/fhir/sid/icd-10'
CPT = 'http://www.ama-assn.org/go/cpt'

RECOGNIZED = [LOINC, SNOMED, RXNORM, ICD10, CPT]

# Enumerating all the FHIR systems here would be a waste of time,
# so load them from the constructed json file.
VALUE_SETS = []
with open('./data/fhir/systems.json') as fhir_handle:
    RECOGNIZED += json.load(fhir_handle)
with open('./data/fhir/daf.json') as daf_handle:
    VALUE_SETS += json.load(daf_handle)
with open('./data/fhir/argo.json') as argo_handle:
    VALUE_SETS += json.load(argo_handle)

# Instantiate the bloom filter.
with open('./data/codes.bf', 'rb') as handle:
    BLOOM = ScalableBloomFilter.fromfile(handle)


def validate_coding(coding):
    """ If the coding system is recognized, check the code.
    """
    if coding.get('system') not in RECOGNIZED:
        raise SystemNotRecognized(coding.get('system'))

    if not coding.get('code'):
        return False

    key = coding['system'] + '|' + coding['code']

    return key in BLOOM


def validate_code(code, system):
    """ If the system is recognized, check the code.
    """
    if (system not in RECOGNIZED) and (system not in VALUE_SETS):
        raise SystemNotRecognized(system)

    key = system + '|' + code

    return key in BLOOM


class SystemNotRecognized(Exception):
    """ Handle unrecognized systems.
    """
