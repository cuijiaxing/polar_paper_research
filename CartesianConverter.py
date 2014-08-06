import cv2
import numpy as np
import math


class CartesianConverter:

    @staticmethod
    def convertCoordinates(r, angle, centroid):
        x = r * cos(angle) + centroid[0]
        y = r * sin(angle) - centroid[1]
        return x, y


    @staticmethod
    def covnertToCartesian3(inputImage, centroid, maxLength, outputWidth = 480, outputHeight = 640):
        '''
        the input image has to be color image
        '''
        outputImage = np.zeros((outputHeight, outputWidth, 3), np.uint8)
        width = inputImage.shape[1]
        height = inputImage.shape[0]
        polarMax = min([j for j in xrange(height), i in xrange(width) if inputImage[j, i, 0] > 0 or inputImage[j, i, 1] != 0 or
                                                                inputImage[j, i, 2] != 0])
        ratio = maxLength * 1.0 / polarMax
        for i in xrange(height):
            for j in xrange(width):
                if inputImage[i, j] > 0:
                    x, y = covnertCoordinates(i * ratio, j, centroid)
                    outputImage[y, x, :] = inputImage[i, j, :]
        return outputImage


    @staticmethod
    def convertToCartesian(inputImage, centroid, maxLength, outputWidth = 480, outputHeight = 640):
        '''
        the input image has to be grayscale image
        '''
        outputImage = np.zeros((outputHeight, outputWidth, 1), np.uint8)
        width = inputImage.shape[1]
        height = inputImage.shape[0]
        polarMax = min([j for j in xrange(height), i in xrange(width) if inputImage[j, i] > 0])
        ratio = maxLength * 1.0 / polarMax
        for i in xrange(height):
            for j in xrange(width):
                if inputImage[i, j] > 0:
                    x, y = covnertCoordinates(i * ratio, j, centroid)
                    outputImage[y, x] = inputImage[i, j]
        return outputImage


