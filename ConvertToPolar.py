import cv2
import math
import numpy as np


def calculateDistance(firstPoint, centroid):
    return math.sqrt((centroid[0] - firstPoint[0, 0])**2 + (centroid[1] - firstPoint[0, 1])**2)

def findMaximumR(points, centroid):
    maxDistance = 0
    distanceList = []
    for point in points:
        distance = calculateDistance(point, centroid)
        distanceList.append(distance)
        maxDistance = max(distance, maxDistance)
    return distanceList, maxDistance





def convertToPolarImage(points, centroid, imageHeight = 500, imageWidth = 360):
    distanceList, maxDistance = findMaximumR(points, centroid)
    angleList = []
    scaleFactor = imageHeight / maxDistance
    outputImage = np.zeros((imageHeight, imageWidth), np.uint8)
    prevR = 0
    prevAngle = 0
    connectBottomIndex = 0
    for i in xrange(len(points) + 1):
        i = i % len(points)
        angle = math.atan2(points[i][0, 1] - centroid[1], points[i][0, 0] - centroid[0])
        r  = distanceList[i] * scaleFactor
        #reverse the images
        r = imageHeight - r
        angle = (angle + 3.1415) * 180 / 3.1415

        if prevR > 0 and abs(angle - prevAngle) < 30:
            cv2.line(outputImage, ((int)(prevAngle), (int)(prevR)), ((int)(angle), (int)(r)), (255, 255, 255))
        else:
            if abs(angle - prevAngle):
                connectBottomIndex = i
        prevAngle = angle
        prevR = r

    

    return outputImage



