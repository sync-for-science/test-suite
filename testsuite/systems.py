import csv
import json
import logging


LOINC = 'http://loinc.org'


def validate_coding(coding):
    if coding['system'] not in [LOINC]:
        return True

    if coding['system'] == LOINC:
        with open('./data/loinc.csv') as handle:
            reader = csv.DictReader(handle)

            for row in reader:
                if coding['code'] == row['LOINC_NUM']:
                    return True
        return False

    return False
