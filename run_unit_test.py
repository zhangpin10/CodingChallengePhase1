import sys
import os
import csv
import h5py
import numpy as np
sys.path.append('../')
from data_parser import DataParser

class UnitTest:
    _data_path = 'unit_test/data'
    _baseline_path = 'unit_test/baseline'
    _result_path = 'unit_test/results'

    def __init__(self, link):
        self._link = link

    def test_DataParser_parse_sample(self):
        data_parser = DataParser(' ')
        for line in self._link:
            try:
                """ generate results """
                dicom_file_path = os.path.join(self._data_path, line)
                contour_file_path = os.path.join(self._data_path, self._link[line])
                shape, img, mask, contour = data_parser.parse_sample(dicom_file_path, contour_file_path)
                np.savez(os.path.join(self._result_path, os.path.splitext(line)[0]) +'.npz', shape=shape, img=img, mask=mask, contour=contour)

                """ Load baseline and do the comparison """
                baseline = np.load(os.path.join(self._baseline_path, os.path.splitext(line)[0]) +'.npz')
                equal1 = np.array_equal(baseline['shape'], shape)
                equal2 = np.array_equal(baseline['img'], img)
                equal3 = np.array_equal(baseline['mask'], mask)
                equal4 = np.array_equal(baseline['contour'], contour)
                if(not(equal1 and equal2 and equal3 and equal4)):
                    return False
            except:
                return False

        return True

            
    def test_DataParser_save_sample(self):
        data_parser = DataParser(' ')
        data_parser.set_result_path(self._result_path)
        for line in self._link:
            try:
                """ generate results """
                dicom_file_path = os.path.join(self._data_path, line)
                contour_file_path = os.path.join(self._data_path, self._link[line])
                shape, img, mask, contour = data_parser.parse_sample(dicom_file_path, contour_file_path)
                data_parser.save_sample(os.path.splitext(line)[0], shape, img, mask, contour)

                """ Load baseline and do the comparison """
                with h5py.File(os.path.join(self._baseline_path, 'data.h5'), 'r') as hf:
                    sample = hf[os.path.splitext(line)[0]]
                    equal1 = np.array_equal(np.array(sample['shape']), shape)
                    equal2 = np.array_equal(np.array(sample['img']), img)
                    equal3 = np.array_equal(np.array(sample['mask']), mask)
                if(not(equal1 and equal2 and equal3)):
                    return False
            except:
                return False

        return True


def parseLink(link_file):
    with open(link_file) as f:
        reader = csv.reader(f, delimiter=',')
        link_pairs = list(reader)
        link = {}
        for line in link_pairs:
            if len(line) == 2:
                link[line[0]] = line[1]
        return link

if __name__ == '__main__':
    link = parseLink('./unit_test/link.csv')

    unit_test = UnitTest(link);

    if unit_test.test_DataParser_parse_sample():
        print('Succeed    DataParser::parse_sample()')
    else:
        print('Failed     DataParser::parse_sample()')

    if unit_test.test_DataParser_save_sample():
        print('Succeed    DataParser::save_sample()')
    else:
        print('Failed     DataParser::save_sample()')


    


