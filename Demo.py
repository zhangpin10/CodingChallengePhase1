import os
from data_loader import BatchIterator
from data_parser import DataParser
from verification_plotter import OverlappingPlot

""" demo for data parser and data loader pipeline """
if __name__ == '__main__':
    
    data_path = 'C:\\CodingChallengePhase1\\final_data'
    visual_result_path = 'visual_results'


    """ demo for data parser pipeline """
    data_parser = DataParser(data_path)
    # set verify to draw verification image which is 
    # the overlap of dicom image, contour and mask
    data_parser.verify = 1   
    #data_parser.parse()


    """ demo for data loader pipeline """
    batch_size = 8
    epochs = 2
    batch_iterator = BatchIterator('data.h5', batch_size, epochs)
    while(1):
        batch = batch_iterator.next()
        if (batch is None):
            break

        # save the verification images
        for b in range(batch_size):
            overlap_file = 'loader_' + batch['name'][b] + '.png'
            overlap_file = os.path.join(visual_result_path, overlap_file)
            overlap_plt = OverlappingPlot(overlap_file, batch['img'][b], batch['mask'][b])
            overlap_plt.save()





    