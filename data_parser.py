"""Parsing code for DICOMS and contour files"""

import os
import sys
import csv
import h5py
import logging
import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
from PIL import Image, ImageDraw 
from verification_plotter import OverlappingPlot

logging.basicConfig(filename='parser.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

class DataParser():
    
    def __init__(self, data_path):
        self._data_path = data_path   
        self._link_file = os.path.join(data_path, 'link.csv')
        self._dicoms = os.path.join(data_path,'dicoms')
        self._contour = os.path.join(data_path, 'contourfiles')
        self._visual_result_path = 'visual_results' # the path for verification images
        self._link = {}                             # the link between dicom folder and contour folder
        self._result_file = 'data.h5'
        self.verify = 0                             # flag for generating verification images

    def set_result_path(self, result_path):
         """ Set the path for .h5 result """
         self._result_file = os.path.join(result_path, 'data.h5')

    def _parseLink(self):
        """ Parse the link between dicom folder and contour folder"""
        with open(self._link_file) as f:
            reader = csv.reader(f, delimiter=',')
            link_list = list(reader)
            for line in link_list[1:]:
                if len(line) == 2:
                    self._link[line[0]] = line[1]

    def _convert_dicomfile_name(self, contour_file):
        """ Generate a dicom file name from a corresponding contour file name"""
        converted_filename=''
        try:
            if(contour_file[0:2] == '._'): converted_filename = '._'
            contour_file = contour_file[2:]
            for i in range(2):
                pos = contour_file.find('-')
                contour_file = contour_file[pos + 1:]
            pos = contour_file.find('-')
            contour_file = contour_file[0:pos]
            dicom_name = str(int(contour_file))
            converted_filename += dicom_name + '.dcm'
        except:
            return None

        return converted_filename

    def _parse_dicom_file(self, filename):
        """Parse the given DICOM filename

        :param filename: filepath to the DICOM file to parse
        :return: dictionary with DICOM image data
        """

        try:
            dcm = pydicom.read_file(filename)
            dcm_image = dcm.pixel_array

            try:
                intercept = dcm.RescaleIntercept
                slope = dcm.RescaleSlope
            except AttributeError:
                intercept = 0
                slope = 1
                
            dcm_image = dcm_image*slope + intercept
            dcm_dict = {'pixel_data' : dcm_image}
            return dcm_dict
        except InvalidDicomError:
            return None

    def _parse_contour_file(self, filename):
        """Parse the given contour filename

        :param filename: filepath to the contourfile to parse
        :return: list of tuples holding x, y coordinates of the contour
        """

        coords_lst = []

        with open(filename, 'r') as infile:
            try:
                for line in infile:
                    coords = line.strip().split()   
                    x_coord = float(coords[0])
                    y_coord = float(coords[1])
                    coords_lst.append((x_coord, y_coord))
            except:
                return None

        return coords_lst

    def _poly_to_mask(self, polygon, width, height):
        """Convert polygon to mask

        :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
         in units of pixels
        :param width: scalar image width
        :param height: scalar image height
        :return: Boolean mask of shape (height, width)
        """

        # http://stackoverflow.com/a/3732128/1410871
        img = Image.new(mode='L', size=(width, height), color=0)
        ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
        mask = np.array(img).astype(bool)
        return mask

    def _save(self, key, data, group):
        """ Add or replace a key valye in a group."""
        if key in group:
          del group[key]
        group[key] = data

    def delete_sample(self, sample_name,):
        """ Delete a sample from the result .h5 file"""
        with h5py.File(self._result_file, 'a') as hf:
            if sample_name in hf:
                del hf[sample_name]

    def save_sample(self, sample_name, shape, img, mask, contour):
        """ Add or replace a sample in the result .h5 file

        :param sample_name: the sample name recorded in the result
        :param shape: the shape of the dicom image
        :param img: parsed dicom image data
        :param contour: the parsed contour. It is used for verification
        """
        with h5py.File(self._result_file, 'a') as hf:
            if sample_name not in hf:
                sample = hf.create_group(sample_name)

            sample = hf[sample_name]
            self._save('shape', np.array(shape), sample)
            self._save('img', img, sample)
            self._save('mask', mask, sample)

        """ Output verification images into the visual_results folder """
        if(self.verify == 1):
            overlap_file =  'parser_' + sample_name + '.png'
            overlap_file = os.path.join(self._visual_result_path, overlap_file)
            overlap_plt = OverlappingPlot(overlap_file, img, mask, contour)
            overlap_plt.save()

    def parse_sample(self, dicom_file_path, contour_file_path):
        """ Add or replace a sample in the result .h5 file

        :param dicom_file_path: 
        :param contour_file_path: 
        :return shape: 
        :return img: 
        :return mask:
        :return contour:
        """

        img = self._parse_dicom_file(dicom_file_path)
        contour = self._parse_contour_file(contour_file_path)

        if(img is None or contour is None):
            logging.warning(' Reading data or ground truth failed!   ' + dicom_file_path + '   ' + contour_file_path)
            return [None, None, None, None]
        else:
            shape = img['pixel_data'].shape
            mask = self._poly_to_mask(contour, shape[0], shape[1])
            if(mask is None):
                logging.warning('poly_to_mask failed!   ' + contour_file_path)
                return [None, None, None, None]
            return [shape, img['pixel_data'], mask, contour] 

    def parse(self):
        """ parse all the dicom files with corresponding contour files"""
        self._parseLink()
        
        for line in self._link:
            """ parse the files under each folder """
            dicom_folder = os.path.join(self._dicoms, line)
            contour_folder = os.path.join(self._contour, self._link[line], 'i-contours')

            if (os.path.isdir(dicom_folder) and os.path.isdir(contour_folder)):
               for contour_file in os.listdir(contour_folder):

                   """ find dicom and contour file pair """
                   dicom_file = self._convert_dicomfile_name(contour_file)
                   dicom_file_path = os.path.join(dicom_folder, dicom_file)
                   contour_file_path = os.path.join(contour_folder, contour_file)

                   if (os.path.exists(dicom_file_path) or os.path.exists(contour_file_path)):
                       """ parse and save a pair of dicom file and corresponding contour file"""
                       print('parsing ' + dicom_file_path)
                       shape, img, mask, contour = self.parse_sample(dicom_file_path, contour_file_path)
                       if(img is not None):
                           sample_name = os.path.basename(dicom_folder) + '-' + os.path.splitext(dicom_file)[0]
                           self.save_sample(sample_name, shape, img, mask, contour)
                   else: 
                       logging.warning(' The data or ground truth does not exist!   ' + dicom_file_path + '   ' + contour_file_path)
                       


