import cv2 as cv
import numpy


class StereoscopicCamera:
    def __init__(self):
        # Stores values important to stereo image handling
        self.halfRows = 0
        self.halfCols = 0

    # stores a color copy of a view
    def storeColorImages(self, image):
        left, right = image

        self.leftColor = left
        self.rightColor = right

        return left, right

    # returns the color copies
    def getColorImages(self):
        return self.leftColor, self.rightColor

    # splits the stereo image
    def splitImage(self, image):
        # get the stereo image
        rawRows, rawCols, rawChannels = image.shape

        # calculate the split line
        self.halfRows = int(rawRows / 2)
        self.halfCols = int(rawCols / 2)

        # split the image in half, or into two views
        leftImg = image[:, :self.halfCols]
        rightImg = image[:, self.halfCols:]

        return leftImg, rightImg

    # converts two stereo views from color to grayscale
    def setImagesGrayscale(self, images):
        left, right = images

        left = cv.cvtColor(left, cv.COLOR_RGB2GRAY)
        right = cv.cvtColor(right, cv.COLOR_RGB2GRAY)

        return left, right

    # displays both views
    def displayImages(self, images):
        leftPic, rightPic = images

        cv.imshow("Left Image", leftPic)
        cv.imshow("Right Image", rightPic)

    # finds the chessboard corners in a view
    def findChessboard(self, images):
        leftImg, rightImg = images

        # This finds the corners of the pattern I used
        foundLeft, leftCorners = cv.findChessboardCorners(leftImg, (6, 19), None)
        foundRight, rightCorners = cv.findChessboardCorners(rightImg, (6, 19), None)

        # This determines when the sub-pixel finder will finish
        # This waits until the error is below 0.001 pixels
        self.termCriteria = (cv.TERM_CRITERIA_EPS, 30, 0.001)

        # Finds chessboard corners to a high degree of accuracy
        # This improves the calibration accuracy
        leftSubCorners = cv.cornerSubPix(leftImg, leftCorners, (14, 14), (-1, -1), self.termCriteria)
        rightSubCorners = cv.cornerSubPix(rightImg, rightCorners, (14, 14), (-1, -1), self.termCriteria)

        print(str(foundLeft) + " " + str(foundRight))

        #draw the corners on the image for evaluation
        cv.drawChessboardCorners(self.leftColor, (6, 19), leftSubCorners, foundLeft)
        cv.drawChessboardCorners(self.rightColor, (6, 19), rightSubCorners, foundRight)

        return leftSubCorners, rightSubCorners
