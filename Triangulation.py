import cv2 as cv
import KeypointDetector as kptDec
import StereoscopicCamera as stereo
import numpy as np

class Triangulator:
    def __init__(self):
        """
        Load in  the essential matrices for triangulation,
        and output those associated matrices for debugging purposes
        Also Initialize important variables
        """
        # Load in  the essential matrices for triangulation,
        self.rotMtx = np.load("Matrices/RotMtx.npy")
        self.transMtx = np.load("Matrices/Translation.npy")
        self.rightCamMtx = np.load("Matrices/rightCamMtx.npy")
        self.leftCamMtx = np.load("Matrices/leftCamMtx.npy")

        self.rightDistCoeff = np.load("Matrices/RDistCoeff.npy")
        self.leftDistCoeff = np.load("Matrices/LDistCoeff.npy")
        self.rightProjMtx = np.load("Matrices/RightProjMtx.npy")
        self.leftProjMtx = np.load("Matrices/LeftProjMtx.npy")

        # Instantiate the objects that will find the keypoints and handle stereo camera stuff
        self.ledDect = kptDec.KeypointDetector()
        self.cam = stereo.StereoscopicCamera()

        #Output all the matrices for debugging purposes
        print(self.rightCamMtx)
        print(self.rightProjMtx)
        print(self.rightDistCoeff)
        print()

        print(self.leftCamMtx)
        print(self.leftProjMtx)
        print(self.leftDistCoeff)
        print()

        print(self.rotMtx)
        print(self.transMtx)

        print("\n----Arrays Loaded----\n")

    # Triangulates the position
    def triangulatePosition(self, lKeypoint, rKeypoint, printPos=False, undistort=False):
        if undistort: # uses the distortion matrix to correct points, sometimes adversely
            outLeft = cv.undistortPoints(lKeypoint.pt, self.leftCamMtx, self.leftDistCoeff)
            outRight = cv.undistortPoints(rKeypoint.pt, self.rightCamMtx, self.rightDistCoeff)
        else:
            outLeft = lKeypoint.pt
            outRight = rKeypoint.pt

        # get the homogenous position coordinates, rotation and magnitude
        rawPos = cv.triangulatePoints(self.leftProjMtx, self.rightProjMtx, outLeft, outRight)
        x, y, z, w = rawPos

        # correct the magnitude
        w = 1/(((1/w)-8.6635)/1.381)

        if printPos:
            print("Raw pos: ")
            print(rawPos)

        # convert the homogenous coordinates to 3D coordinates
        pos = np.array([(x/w), (y/w), (z/w)], np.float32)

        if printPos:
            print("\nCalculated Pos: ")
            print(pos)

        return pos, rawPos

    # Filters the found points
    def filterKeypoints(self, points):
        outputPoint = 0

        for keypoint in points:
            x, y = keypoint.pt
            if outputPoint == 0:
                outputPoint = keypoint

            currX, currY = outputPoint.pt

            # The point that moved less than 100 pixels is likely the one we want
            if abs(currX - x) < 100 and abs(currY - y) < 100:
                outputPoint = keypoint
            if cv.waitKey(1) == ord('r'): # This protects from locking on to the wrong point
                outputPoint = keypoint

        return outputPoint

    def getPosition(self, videoCap):
        # stores the position and the homogenous coordinates of the position
        position = np.zeros((1, 3), np.float32)
        homoPos = np.zeros((1, 4), np.float32)

        isReturned, frame = videoCap.read()

        leftEye, rightEye = self.cam.splitImage(frame)

        # look for bright points
        leftEyeFinal, leftPoints = self.ledDect.findKeyPoints(leftEye)
        rightEyeFinal, rightPoints = self.ledDect.findKeyPoints(rightEye)

        outputLeftPoint = self.filterKeypoints(leftPoints)
        outputRightPoint = self.filterKeypoints(rightPoints)

        # Triangulate the position of the bright point
        if outputRightPoint != 0 and outputLeftPoint != 0:
            position, homoPos = self.triangulatePosition(outputLeftPoint, outputRightPoint)

        return position, homoPos

    # Draws a window with position information
    def displayPositionInfo(self, winName, posInfo):
        # clear the window and draw the position information on top
        blackImg = np.zeros((50, 1000, 3), np.float32)
        editedImg = cv.putText(self.blackImg, posInfo, (0, 22), cv.QT_FONT_NORMAL, 0.7, (255, 255, 255), lineType=cv.LINE_AA)

        # display the image
        cv.imshow(winName, editedImg)
