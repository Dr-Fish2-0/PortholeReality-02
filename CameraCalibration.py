import cv2 as cv
import numpy as np
import glob
import StereoscopicCamera

# load in the calibration images and intialize the stereo camera
images = glob.glob("C:/Users/Dr.Fish/Pictures/WindowedReality/Landscape/*.jpg")
stereoCam = StereoscopicCamera.StereoscopicCamera()

#
# I used a lot of boilerplate code from OpenCV, there are only so many ways to calibrate a camera
#
# Stores the points of the pattern in real world space relative to the top left corner
patternPoints = np.zeros((6 * 19, 3), np.float32)
patternPoints[:, :2] = np.mgrid[0:142.8:23.8, 0:452.2:23.8].T.reshape(-1, 2)

# Two arrays that store the pixel coordinates of the pattern's corners
leftCorners = []
rightCorners = []

# Stores the pattern points for each calibration image
patPoints = []

# gets all the chessboard corners and stores the coordinates in the arrays
for calibImg in images:
    # read in the image,
    # split the views, store color copies, and convert them to grayscale
    img = cv.imread(calibImg)
    imageSet = stereoCam.setImagesGrayscale(stereoCam.storeColorImages(stereoCam.splitImage(img)))

    # gets the pixel coordinates of the chessboard corners
    leftRawCorners, rightRawCorners = stereoCam.findChessboard(imageSet)

    # Add in the pixel and world coordinates to their arrays
    leftCorners.append(leftRawCorners)
    rightCorners.append(rightRawCorners)
    patPoints.append(patternPoints)

# Calibrate both cameras
leftRet, leftCameraMtx, leftDistCoeff, leftRot, leftTrans = cv.calibrateCamera(patPoints, leftCorners, imageSet[0].shape[::-1], None, None, criteria=stereoCam.termCriteria)
rightRet, rightCameraMtx, rightDistCoeff, rightRot, rightTrans = cv.calibrateCamera(patPoints, rightCorners, imageSet[1].shape[::-1], None, None, criteria=stereoCam.termCriteria)

# Ensures that the camera matrices and distortion coefficients are untouched
calibrationFlags = (cv.CALIB_FIX_INTRINSIC + cv.CALIB_FIX_K1 + cv.CALIB_FIX_K2 + cv.CALIB_FIX_K3 + cv.CALIB_FIX_K4 + cv.CALIB_FIX_K5 + cv.CALIB_FIX_K6)

# Calibrate the stereoscopic camera
# This provides projection matrices to be used for triangulation
stereoInfo = cv.stereoCalibrate(patPoints, leftCorners, rightCorners, leftCameraMtx, leftDistCoeff, rightCameraMtx, rightDistCoeff, imageSize=imageSet[0].shape[::-1])

# Rotation, translation, and projection matrices
rot = stereoInfo[5]
trans = stereoInfo[6]
leftProjMtx = stereoInfo[1]
rightProjMtx = stereoInfo[3]

# Store these matrices for later use
np.save("Matrices/LeftCamMtx.npy", leftCameraMtx)
np.save("Matrices/RightCamMtx.npy", rightCameraMtx)
np.save("Matrices/RotMtx.npy", rot)
np.save("Matrices/Translation.npy", trans)
np.save("Matrices/RDistCoeff.npy", stereoInfo[2])
np.save("Matrices/LDistCoeff.npy", stereoInfo[4])

np.save("Matrices/LeftProjMtx.npy", leftProjMtx)
np.save("Matrices/RightProjMtx.npy", rightProjMtx)

# Print out error and matrices obtained in calibration
print("\nPixel Error:")
print(stereoInfo[0])

print("\nRot:")
print(rot)

print("\nTransform:")
print(trans)

print()
print(leftProjMtx)
print(rightProjMtx)

print("\nLeft Matrix: ")
print(leftCameraMtx)
print(leftDistCoeff)

print("\nRight Matrix: ")
print(rightCameraMtx)
print(rightDistCoeff)

cv.waitKey(0)
cv.destroyAllWindows()
