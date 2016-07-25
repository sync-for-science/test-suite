from pybloom import ScalableBloomFilter


LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'


def bf_provider(func):
    with open('./data/codes.bf', 'rb') as handle:
        bloom = ScalableBloomFilter.fromfile(handle)

    def func_wrapper(*args, **kwargs):
        return func(bloom, *args, **kwargs)

    return func_wrapper


@bf_provider
def validate_coding(bloom, coding):
    if coding.get('system') not in [LOINC, SNOMED]:
        return True

    key = coding['system'] + '|' + coding['code']

    return key in bloom
