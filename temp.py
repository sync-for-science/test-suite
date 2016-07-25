import csv

from pybloom import ScalableBloomFilter

LOINC = 'http://loinc.org'
SNOMED = 'http://snomed.info/sct'


bf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)

with open('./data/snomed/SnomedCT_RF2Release_INT_20160131/Full/Terminology/sct2_Concept_Full_INT_20160131.txt') as handle:
    reader = csv.DictReader(handle, delimiter='\t')

    for row in reader:
        bf.add(SNOMED + '|' + row['id'])

with open('./data/loinc.csv') as handle:
    reader = csv.DictReader(handle)

    for row in reader:
        bf.add(LOINC + '|' + row['LOINC_NUM'])

with open('./data/codes.bf', 'wb') as handle:
    bf.tofile(handle)
