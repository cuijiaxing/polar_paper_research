import cv2
import numpy as np
import math


class CartesianConverter:

    @staticmethod
    def convertCoordinates(r, angle, centroid):
        x = centroid[0] - r * math.cos(angle * 3.1415926 / 180)
        y = centroid[1] - r * math.sin(angle * 3.1415926 / 180)
        return x, y


    @staticmethod
    def convertToCartesian3(inputImage, centroid, maxLength, outputWidth = 640, outputHeight = 480):
        '''
        the input image has to be color image
        '''
        outputImage = np.zeros((outputHeight, outputWidth, 3), np.uint8)
        width = inputImage.shape[1]
        height = inputImage.shape[0]
        polarMax = height
        ratio = maxLength * 1.0 / polarMax
        print ratio
        for i in xrange(height):
            for j in xrange(width):
                if inputImage[i, j].any() > 0:
                    x, y = CartesianConverter.convertCoordinates((height - i - 1) * ratio, j, centroid)
                    outputImage[y, x, :] = inputImage[i, j, :]
        return outputImage


    @staticmethod
    def convertToCartesian(inputImage, centroid, maxLength, outputWidth = 640, outputHeight = 480):
        '''
        the input image has to be grayscale image
        '''
        outputImage = np.zeros((outputHeight, outputWidth, 1), np.uint8)
        width = inputImage.shape[1]
        height = inputImage.shape[0]
        polarMax = height
        ratio = maxLength * 1.0 / polarMax
        for i in xrange(height):
            for j in xrange(width):
                if inputImage[i, j] > 0:
                    x, y = CartesianConverter.convertCoordinates((height - i - 1) * ratio, j, centroid)
                    outputImage[y, x] = inputImage[i, j]
        return outputImage


