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


def convertToPolarImageWithInterpolation(points, centroid, filled = True, imageHeight = 500, imageWidth = 360):
    distanceList, maxDistance = findMaximumR(points, centroid)
    angleList = []
    rList = []
    scaleFactor = imageHeight / maxDistance
    outputImage = np.zeros((imageHeight, imageWidth), np.uint8)
    prevR = 0
    prevAngle = 0
    connectBottomIndex = 0
    maxR = 0
    for i in xrange(len(points) + 1):
        i = i % len(points)
        angle = math.atan2(points[i][0, 1] - centroid[1], points[i][0, 0] - centroid[0])
        r  = distanceList[i] * scaleFactor
        #reverse the images
        r = imageHeight - r
        angle = (angle + 3.1415) * 180 / 3.1415
        rList.append(r)
        angleList.append(angle)
        if prevR > 0 and abs(angle - prevAngle) > 200:
            connectBottomIndex = i
        prevAngle = angle
        prevR = r

    prevIndex = (connectBottomIndex - 1 + len(points)) % len(points)
    #added_y = [imageHeight - 1, imageHeight - 1, imageHeight - 1]
    #added_x = [angleList[prevIndex], 180, angleList[connectBottomIndex]]

    added_y = [rList[prevIndex], imageHeight - 1, imageHeight - 1, imageHeight - 1, rList[connectBottomIndex]]
    added_x = [0, 0, 180, 359, 359]
    rList = rList[0 : prevIndex + 1] + added_y + rList[prevIndex + 1 : ]
    angleList = angleList[0 : prevIndex + 1] + added_x + angleList[prevIndex + 1 : ]
    points = np.zeros((len(angleList), 1, 2), np.int)

    for i in xrange(len(angleList)):
        points[i, 0, 0] = angleList[i]
        points[i, 0, 1] = rList[i]

    contours = [points]

    if filled:
        cv2.drawContours(outputImage, contours, 0, (255, 255, 255), cv2.cv.CV_FILLED)
    else:
        cv2.drawContours(outputImage, contours, 0, (255, 255, 255))
    return outputImage, maxDistance




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

        if prevR > 0 and abs(angle - prevAngle) < 200:
            cv2.line(outputImage, ((int)(prevAngle), (int)(prevR)), ((int)(angle), (int)(r)), (255, 255, 255))
        else:
            if prevR > 0 and abs(angle - prevAngle) > 200:
                connectBottomIndex = i
        prevAngle = angle
        prevR = r

    return outputImage, maxDistance



