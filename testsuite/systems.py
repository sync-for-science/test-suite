""" Validate provided codes.
"""
from pybloom import ScalableBloomFilter


LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'
RXNORM = 'http://www.nlm.nih.gov/research/umls/rxnorm'
ICD10 = 'http://hl7.org/fhir/sid/icd-10'


def bf_provider(func):
    """ Decorator for the validate_coding method so that we only have to
    instantiate the bloom filter once.
    """
    with open('./data/codes.bf', 'rb') as handle:
        bloom = ScalableBloomFilter.fromfile(handle)

    def func_wrapper(*args, **kwargs):
        """ Wrapper function.
        """
        return func(bloom, *args, **kwargs)

    return func_wrapper


@bf_provider
def validate_coding(bloom, coding):
    """ If the coding system is recognized, check the code.
    """
    if coding.get('system') not in [LOINC, SNOMED, RXNORM, ICD10]:
        return True

    key = coding['system'] + '|' + coding['code']

    return key in bloom
