""" Validate provided codes.
"""
import json

from pybloom import ScalableBloomFilter


LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'
RXNORM = 'http://www.nlm.nih.gov/research/umls/rxnorm'
ICD10 = 'http://hl7.org/fhir/sid/icd-10'

RECOGNIZED = [LOINC, SNOMED, RXNORM, ICD10]

# Enumerating all the FHIR systems here would be a waste of time,
# so load them from the constructed json file.
with open('./data/fhir/systems.json') as fhir_handle:
    RECOGNIZED += json.load(fhir_handle)
with open('./data/fhir/daf.json') as daf_handle:
    RECOGNIZED += json.load(daf_handle)


def bf_provider(func):
    """ Decorator for the validate_coding method so that we only have to
    instantiate the bloom filter once.
    """
    with open('./data/codes.bf', 'rb') as handle:
        func.bloom = ScalableBloomFilter.fromfile(handle)

    return func


@bf_provider
def validate_coding(coding):
    """ If the coding system is recognized, check the code.
    """
    if coding.get('system') not in RECOGNIZED:
        return True

    if not coding.get('code'):
        return False

    key = coding['system'] + '|' + coding['code']

    return key in validate_coding.bloom
