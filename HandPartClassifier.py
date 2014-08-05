import cv2
import numpy as np
import random

class HandPartClassifier:
    @staticmethod
    def showClassImage(window_name, inputImage):

        height = inputImage.shape[0]
        width = inputImage.shape[1]

        classMap = np.zeros((height, width, 3), np.uint8)
        colorMap = {}

        for i in xrange(height):
            for j in xrange(width):
                c = inputImage[i, j]
                if c == 0:
                    classMap[i, j, :] = 0
                
                if not c in colorMap:
                    colorMap[c] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))#colorArray[c % COLOR_NUM];

                color = colorMap[c];
                classMap[i, j, 0] = color[0]
                classMap[i, j, 1] = color[1]
                classMap[i, j, 2]= color[2]

        cv2.imshow(window_name, classMap);
        return classMap

    #not all of the pixel values are either 0 or 255, some of them may be 1, 2, 3, or 252 and so on.
    @staticmethod
    def fixImage(inputImage, lower_value, upper_value ):
        cv2.threshold(inputImage,inputImage, lower_value, upper_value, THRESH_BINARY);
        return inputImage;

    @staticmethod
    def findLength(inputImage, x, y, left, right):
        currentClass = inputImage[y, x]
        length = 1
        left = x
        right = x
        while left >= 0:
            if inputImage[y, left] == currentClass:
                --left
            else:
                break

        while right < inputImage.cols:
            if inputImage[y, right] == currentClass:
                ++right
            else:
                break

        ++left;
        --right;
        return right - left + 1, left, right

    @staticmethod
    def fillLine(inputImage, y, left, right, class_num):
        for i in xrange(left, right + 1):
            inputImage[y, i] = class_num

        return inputImage


    @staticmethod
    def bottomUp(inputImage):
        prev_class = 0;
        current_class = 0;
        prev_left = 0
        prev_right = 0
        current_left = 0
        current_right = 0
        prev_length = 0
        current_length = 0
        width = inputImage.shape[1]
        height = inputImage.shape[0]

        palm_length = width;
        palm_class = 0;
        has_hand = False;
        for j in xrange(0, width):
            prev_class = inputImage[height - 1, j]
            if not has_hand:
                temp_length, prev_left, prev_right = HandPartClassifier.findLength(inputImage, j, height - 1, prev_left, prev_right);
                if temp_length > palm_length/ 2 : 
                    palm_class = prev_class
                    has_hand = True
                    palm_length = temp_length

            #index begins from number of rows - 2 to 0
            for i in xrange(height - 2, -1):
                prev_class = inputImage[i +1 , j]
                current_class = inputImage[i, j]
                if prev_class != current_class and prev_class != 0 and current_class != 0 :
                    current_length, current_left, current_right = findLength(inputImage,j, i, current_left, current_right)
                    #ofs<< i <<" "<< j <<" " << current_length << std::endl;
                    if prev_class == palm_class and current_length * 1.0 / palm_length < 0.2:
                        continue

                    prev_length, prev_left, prev_right = findLength(inputImage, j, i + 1, prev_left, prev_right);
                    ratio = current_length * 1.0 / prev_length;
                    if (ratio > 0.5) or ratio < 0.1 or current_right - current_left < 5 :
                        inputImage = fillLine(inputImage, i, current_left, current_right, prev_class)
                        #ofs<< i <<" "<< j <<" " << ratio<<" "<<current_length<<" "<<prev_length<<std::endl;

        return inputImage;


    #the first step is to do a rough classification
    @staticmethod
    def roughClassify(inputImage):
        indexArray = [0 for i in xrange(256)]
        classArray = [0 for i in xrange(256)]
        prev_color = 0
        current_color = 0
        startIndex = 0
        endIndex = 0
        height = inputImage.shape[0]
        width = inputImage.shape[1]


        current_class = 1
        for i in xrange(height):
            prev_color = inputImage[i, 0]
            if prev_color == 255:
                startIndex = 0

            for j in xrange(width):
                current_color = inputImage[i, j];
                if prev_color == 0 and current_color == 255:
                    startIndex = j

                if prev_color == 255 and current_color == 0:
                    #here we do back trace
                    endIndex = j - 1
                    current_class += 1
                    if current_class == 256:
                        current_class = 1

                if current_color == 255:
                    inputImage[i, j] = current_class

                prev_color = current_color
                

        return inputImage


    @staticmethod
    def classifyHandParts(inputImage):
        #fix the noise points
        #inputImage = fixImage(inputImage)
        inputImage = HandPartClassifier.roughClassify(inputImage)
        print "rough classify finished!"
        #the season that we have to scan twice it to 
        #avoid  discontinuity. you can try scaning once
        #to see what will happen
        #inputImage = HandPartClassifier.bottomUp(inputImage)
        #inputImage = HandPartClassifier.bottomUp(inputImage)
        HandPartClassifier.showClassImage('classImage', inputImage)
        return inputImage


