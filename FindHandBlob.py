import cv2
from FileNameFeeder import FileNameFeeder
import numpy as np
from ConvertToPolar import convertToPolarImage


def morphological(inputImage):
    kernel = np.ones((5, 5), np.uint8)
    #inputImage = cv2.erode(inputImage, kernel, iterations = 1)
    inputImage = cv2.morphologyEx(inputImage, cv2.MORPH_OPEN, kernel)


def findHandBlob(inputImage, outputImage):
    ret, inputImage = cv2.threshold(inputImage, 40, 255, 0)
    contours, _ = cv2.findContours(inputImage, 
                        cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    maxArea = -1
    maxIndex = 0
    for i in xrange(len(contours)):
        if cv2.contourArea(contours[i]) > maxArea:
            maxArea = cv2.contourArea(contours[i])
            maxIndex = i

    cv2.drawContours(outputImage, contours, maxIndex, (255, 255, 255), cv2.cv.CV_FILLED)
    moments = cv2.moments(contours[maxIndex])

    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        cv2.circle(outputImage, (cx, cy), 5, (0, 0, 0), -1)
    return contours[maxIndex], (cx, cy)


if __name__ == "__main__":
     inputFolder = "test/"
     imageFileNameList = FileNameFeeder.getImageFiles(inputFolder)

     for fileName in imageFileNameList:
        image = cv2.imread(inputFolder + fileName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        blank_image = np.zeros(image.shape, np.uint8)
        morphological(image);
        contours, centroid = findHandBlob(image, blank_image)
        cv2.imshow("after", blank_image)
        cv2.imshow("original", image)
        #cv2.imwrite(inputFolder + "bi_" + fileName, blank_image)
        polarImage = convertToPolarImage(contours, centroid)
        cv2.imshow('ploar', polarImage)
        cv2.imwrite(inputFolder + "po_" + fileName, polarImage)
        cv2.waitKey()
     print "finished!"

