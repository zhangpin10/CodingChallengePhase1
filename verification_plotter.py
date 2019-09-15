import numpy as np
import matplotlib.pyplot as plt

class OverlappingPlot():
    def __init__(self, 
                 filename, 
                 img, 
                 mask, 
                 contour = None):
        self._filename = filename
        self._img = img
        self._mask = mask.astype(int)
        self._contour = contour
 
    def save(self):
        # overlap mask onto dicom image. The mask if yellow
        img_overlap = np.stack([self._img, self._img, (1 - self._mask) * self._img], axis = 2)

        # overlap contour onto dicom image. The contour if red
        if(self._contour is not None):
            for p in self._contour:
                img_overlap[int(round(p[1])), int(round(p[0])), 1] = 0
                img_overlap[int(round(p[1])), int(round(p[0])), 2] = 0

        plt.imshow(img_overlap)  
        plt.savefig(self._filename)


