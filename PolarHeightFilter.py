import cv2

class PolarHeightFilter:

    @staticmethod
    def filterHeight(inputImage, threshold = 10):
        '''
        filter the area whose height is less than the threshold
        '''
        height = inputImage.shape[0]
        width = inputImage.shape[1]

        for i in xrange(width):
            prevColor = 0
            currentColor = inputImage[height - 1, i]
            currentHeight = 0
            for j in reversed(xrange(height)):
                if inputImage[j, i] == currentColor:
                    currentHeight += 1
                else:
                    if currentHeight < threshold:
                        for k in xrange(j - currentHeight, j):
                            inputImage[k, i] = prevColor
                    prevColor = currentColor
                    currentColor = inputImage[i, j]
                    currentHeight = 1
        return inputImage





