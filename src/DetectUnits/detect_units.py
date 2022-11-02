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
# This entire process is predicated on the map images being aligned. This will be done via outpost pixels being read from the entire screen ONCE
def only_heroes():
    # Open HSV image using opencv2
    user_img = cv.imread('./src/DetectUnits/RadiantPOV_Live.png', cv.COLOR_BGR2HSV)
    no_vision = cv.imread('./src/DetectUnits/RadiantPOV_NoVision.png', cv.COLOR_BGR2HSV)
    all_vision = cv.imread('./src/DetectUnits/RadiantPOV_AllVision_Warded.png', cv.COLOR_BGR2HSV)

    # Combine images using mask
    # All pixels  that are in vision because we are filtering the no vision image out
    # mask an image against another image
    vision_pixels = cv.bitwise_and(user_img, (mask_vision_pixels := cv.bitwise_xor(user_img, no_vision)))
    show_img(vision_pixels)
    # We are left with all pixels in vision, we want to filter base vision map out and get all the units
    nonmap_pixels = cv.bitwise_xor(vision_pixels, all_vision)


def show_img(img):
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    only_heroes()
    # Test

