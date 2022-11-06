"""

Heroes:

Masks the minimap pixels against a fully dark minimap with no buildings except the ancients. Each centroid that is not
part of the default minimap gets classified as one of the 9 other players via color detection.

    Player heroes:
        Player's hero is detected via game-state integration.
            OR MSFT BAINT
    Other heroes:
        If a centroid is classified with multiple player colors, then we conclude the players are on top of each other
        and give the coordinates of each player as the center of the centroid + some radius r away from the middle as
        to be able to display multiple circles on top of each other on the coordinates returned.
            OR MSFT BAINT


Towers & structures:

Friendly structures are detected via game-state integration.
    OR MSFT BAINT

Enemy structures are detected via checking for their presence on hardcoded coordinates - hardcoded coordinates exist for
both friendly and enemy teams.
    OR MSFT BAINT


Outposts:

Outposts are in the same position every time. Their parity is decided via color detection.

Couriers, illusion units, creeps, summoned units, map drawings, map pings:

TBD.

 For illusions, maybe just send coordinates and magnitude? That way PL illusion stack is just a bigger colored icon.
    MSFT BAINT
Wards:
    MSFT BAINT

TBD.

"""

# alright goombas, round 4
# this time we get this dub
# dont need ml, dont need ai. just need msft BAINT

"""
GOAL: Find screen of only heroes, and either screen of all vision/no vision (they are complimentary)

Do this using masking:
I: NV_r = No vision, raw image.
I: U_r = User, raw image.
I: AV_r = All vision, raw image.

C: NV_r + U__r = AV_H = Vision + Heroes
C: AV_H ^ AV_r = NV_H = No vision + heroes

C: NV_H & AV_H = H (only heroes)
C: NV_H - H = NV (No vision)
C: AV_H - H = AV (Only vision)


"""
import cv2 as cv
import os
import numpy as np
from util.hsv_thresholder import thresholder
import scipy.ndimage
BASE_ALLVISION_PATH = "./src/DetectUnits/dota_assets/util/8bit259_illuminated_dotamap_border.png"
BASE_NOVISION_PATH = "./src/DetectUnits/dota_assets/util/8bit259_dark_dotamap_border.png"

# This entire process is predicated on the map images being aligned. This will be done via outpost pixels being read from the entire screen ONCE
def only_heroes(user_image, no_vision_image, all_vision_image):
    # Open HSV image using opencv2
        # TODO: Align images programmatically and test robustness of illuminated map using inRange
    # Convert image to HSV
    user_img_hsv = cv.cvtColor(user_image, cv.COLOR_RGB2HSV)
    no_vision_hsv = cv.cvtColor(no_vision_image, cv.COLOR_RGB2HSV)
    all_vision_hsv = cv.cvtColor(all_vision_image, cv.COLOR_RGB2HSV)
    # show_img(user_img_hsv, no_vision_hsv, all_vision_hsv)
    # Combine images using mask
    MASK_MIN = 0 * np.array([1, 1, 1])
    MASK_MAX = 255  * np.array([1, 1, 1])
    mask_novision_pixels = cv.inRange((adpx := cv.absdiff(user_img_hsv, no_vision_hsv)), MASK_MIN, MASK_MAX)
    user_vision_pixels = cv.bitwise_and(user_img_hsv, user_img_hsv, mask=mask_novision_pixels)
    # Only the pixels in the vision image that are in the user image
    base_vision_pixels = cv.bitwise_and(all_vision_hsv, all_vision_hsv, mask=mask_novision_pixels)
    # show_img(user_vision_pixels, base_vision_pixels, adpx)
    # We are left with all pixels in vision, we want to filter base vision map out and get all the units
    mask_nonvision_pixels = cv.inRange((adpx := cv.absdiff(user_vision_pixels, base_vision_pixels)), MASK_MIN, MASK_MAX)
    nonvision_pixels = cv.bitwise_and(user_vision_pixels, user_vision_pixels, mask=mask_nonvision_pixels)
    # show_img(nonvision_pixels, adpx)
    return apply_hsv_bc_transform(nonvision_pixels, hmin=0, alpha=93, beta=0), user_image

def apply_hsv_bc_transform(img, hmin=0, hmax=179, smin=0, smax=255, vmin=0, vmax=255, alpha=100, beta=1):
    # Set minimum and maximum HSV values to display
    # HMin: 30 - to remove tiny pixels (neutrals, artifacts, etc)
    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])

    # Convert to HSV format and color threshold
    # Contrast: 0.93
    # Brightness: 0
    adjusted = cv.convertScaleAbs(img, alpha=(alpha/100), beta=beta)
    mask = cv.inRange(adjusted, lower, upper)
    result = cv.bitwise_and(img, img, mask=mask)
    return result

def show_img(*imgs):
    # Horizontally concatenate images hconcat
    img = cv.hconcat(imgs)
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def detect_objects(img, base_img):
    # Function that uses opencv findContours to find objects in an image
    # Returns a list of contours and a list of bounding boxes
    # img: image to find contours in
    # base_img: image to draw contours on
    # Returns: contours, bounding boxes, base_img
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contours, hierarchy = cv.findContours(grayscale, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        bounding_boxes.append((x, y, w, h))
        cv.rectangle(base_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return contours, bounding_boxes, base_img


def round_two(user_image, no_vision_image, all_vision_image):
    # This function runs threshold wrongly on the base_image and also the vision and dark image
    # And does the same as above
    ret, thresh_usr = cv.threshold(user_image, 141, 255, 0)
    ret, thresh_nv  = cv.threshold(no_vision_image, 127, 255, 0)
    ret, thresh_av = cv.threshold(all_vision_image, 0, 255, 0)
    res, base = only_heroes(thresh_usr, thresh_nv, thresh_nv)
    detect_objects(res, user_img)
    return res, user_image


def slidify_threshold(img):
    # Slidify a function
    # img: image to apply function to
    # fn: function to apply to image
    # Displays window with slider of fn and its changes to the image
    def nothing(x):
        pass

    cv.namedWindow('image')
    trackbar_name_min = 'thresh min'
    trackbar_name_max = 'thresh max'
	# Create trackbars for color change
	# Hue is from 0-179 for Opencv
    cv.createTrackbar(trackbar_name_min, 'image', 0, 255, nothing)
    cv.createTrackbar(trackbar_name_max, 'image', 0, 255, nothing)
    cv.setTrackbarPos(trackbar_name_min, 'image', 0)
    cv.setTrackbarPos(trackbar_name_max, 'image', 255)

    while True:
        # Get current positions of all trackbars
        fnMinVal = cv.getTrackbarPos(trackbar_name_min, 'image')
        fnMaxVal = cv.getTrackbarPos(trackbar_name_max, 'image')

        # Set minimum and maximum HSV values to display

        # Convert to HSV format and color threshold
        _, result = cv.threshold(img, fnMinVal, fnMaxVal, 0)
        cv.imshow('image', result)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    return result


if __name__ == '__main__':
    user_img = cv.imread('./src/DetectUnits/280pxlive.png')
    no_vision = cv.imread(BASE_NOVISION_PATH)
    all_vision = cv.imread(BASE_ALLVISION_PATH)
    # res, img = only_heroes(user_img, no_vision, all_vision)
    res = round_two(user_img, no_vision, all_vision)
    # Test

