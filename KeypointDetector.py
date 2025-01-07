import cv2 as cv


class KeypointDetector:
    def __init__(self):
        # Specify the search filters for the blob detector
        ledParams = cv.SimpleBlobDetector_Params()

        # Thresholds for brightness
        # The minimum is low because of the low ambient light
        ledParams.minThreshold = 5
        ledParams.maxThreshold = 255

        # filters by how round the point is
        ledParams.filterByCircularity = True
        ledParams.minCircularity = 0.5

        # Specifies the minimum size/area the point should take
        ledParams.filterByArea = True
        ledParams.minArea = 3

        # This also filters by brightness, there may be a logic error in OpenCV here
        ledParams.filterByColor = True
        ledParams.blobColor = 255

        # Specify what filters to not use
        ledParams.filterByInertia = False
        ledParams.filterByConvexity = False

        self.ledDetector = cv.SimpleBlobDetector_create(ledParams)

    # Finds the keypoints in the image using the criteria above
    def findKeyPoints(self, image):
        grayImage = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  # convert to grayscale

        keypoints = self.ledDetector.detect(grayImage)  # detect the keypoints

        # return the image and the keypoints
        return image, keypoints

    # Draws text with information about a keypoint on an image.
    def drawPointInfo(self, image, keypoint):
        keyX, keyY = keypoint.pt
        ledPoint = (int(keyX), int(keyY))

        # Draws a circle around the keypoint
        cv.circle(image, ledPoint, int(keypoint.size), (0, 255, 0), 2)

        # All important info is put in a string and drawn on the image
        pointInfo = str(keypoint.size) + " " + str(keypoint) + ": " + str(keypoint.pt)
        cv.putText(image, pointInfo, (0, 11), cv.QT_FONT_NORMAL, 0.3, (255, 255, 255), lineType=cv.LINE_AA)
