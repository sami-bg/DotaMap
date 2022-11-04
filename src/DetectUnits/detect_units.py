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
# This entire process is predicated on the map images being aligned. This will be done via outpost pixels being read from the entire screen ONCE
def only_heroes():
    # Open HSV image using opencv2
    user_img = cv.imread('./src/DetectUnits/SIMPLETEST.png')
    no_vision = cv.imread('./src/DetectUnits/NOVISION.png')
    all_vision = cv.imread('./src/DetectUnits/ALLVISION.png')
    # TODO: Align images programmatically and test robustness of illuminated map using inRange

    # Convert image to HSV
    user_img_hsv = cv.cvtColor(user_img, cv.COLOR_RGB2HSV)
    no_vision_hsv = cv.cvtColor(no_vision, cv.COLOR_RGB2HSV)
    all_vision_hsv = cv.cvtColor(all_vision, cv.COLOR_RGB2HSV)

    # Combine images using mask
    # All pixels  that are in vision because we are filtering the no vision image out
    # mask an image against another image
    MASK_MIN = 8 * np.array([1, 1, 1])
    MASK_MAX = 255  * np.array([1, 1, 1])
    mask_vision_pixels = cv.inRange(cv.absdiff(user_img, no_vision), MASK_MIN, MASK_MAX)
    vision_pixels = cv.bitwise_and(user_img, user_img, mask=mask_vision_pixels)
    show_img(vision_pixels, all_vision, no_vision, user_img)
    show_img(mask_vision_pixels)
    # thresholder(user_img, no_vision, all_vision, img=cv.cvtColor(vision_pixels, cv.COLOR_HSV2RGB))
    # We are left with all pixels in vision, we want to filter base vision map out and get all the units
    mask_nonvision_pixels = cv.inRange(cv.absdiff(vision_pixels, all_vision), MASK_MIN, MASK_MAX)
    nonvision_pixels = cv.bitwise_and(vision_pixels, vision_pixels, mask=mask_nonvision_pixels)
    show_img(nonvision_pixels, all_vision, no_vision)
    show_img(mask_nonvision_pixels)

def show_img(*imgs):
    # Horizontally concatenate images hconcat
    img = cv.hconcat(imgs)
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    only_heroes()
    # Test

