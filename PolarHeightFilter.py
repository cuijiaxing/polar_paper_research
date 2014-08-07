import cv2
import numpy as np

class PolarHeightFilter:

    @staticmethod
    def filterHeight(inputImage, threshold = 30):
        '''
        filter the area whose height is less than the threshold
        '''
        height = inputImage.shape[0]
        width = inputImage.shape[1]
        blackColor = np.zeros((1, 3), np.uint8)
        for i in xrange(width):
            prevColor = blackColor
            currentColor = inputImage[height - 1, i, :]
            currentHeight = 0
            for j in reversed(xrange(height)):
                if inputImage[j, i, :].all() == currentColor.all():
                    currentHeight += 1
                else:
                    if currentHeight < threshold and prevColor.all() != blackColor.all():
                        print j, i, currentHeight
                        for k in xrange(j - currentHeight, j):
                            inputImage[k, i] = prevColor
                    prevColor = currentColor
                    currentColor = inputImage[j, i, :]
                    currentHeight = 1
        return inputImage





