import cv2
import numpy as np
from util.enums import Locations, Colors, Objects, HSVColorThreshold


# Read and merge
def load_img(path: str):
	img = cv2.imread(path)
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	return img_hsv


def classify_enum_unit_type(color: Colors):
	if 'PLAYER' in color.name:
		return 'player'
	if 'TEAM' in color.name:
		return 'team'
	return f'Error: {color.name}'


def create_masks_from_color_thresholds(img):
	masks = []
	for color in Colors.get_all():
		# Get the mask from the color thresholds
		val = color.value
		mask = cv2.inRange(img, val.MIN, val.MAX)
		masks.append(mask)
		unit_type = classify_enum_unit_type(color)
	return masks


def find_centroid_location(mask, unit_type: str):
	ret, thresh = cv2.threshold(mask, 127, 255, 0)
	if unit_type == 'player':
		M = cv2.moments(thresh)
		if M['m00'] == 0:
			return 0, 0
		else:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			return cX, cY
	if unit_type == 'team':
		pass


img_hsv = load_img('./src/DetectUnits/SIMPLETEST.png')
masks = create_masks_from_color_thresholds(img_hsv)

purple_mask = cv2.inRange(img_hsv, Colors.PLAYER_PURPLE.value.MIN, Colors.PLAYER_PURPLE.value.MAX)

cv2.imshow('mask', purple_mask)

for idx, mask in enumerate([purple_mask]):
	res = cv2.bitwise_or(img_hsv, img_hsv, mask)
	cX, cY = find_centroid_location(mask, unit_type='player')
	print(f'{cX}, {cY}')
	# cv2.circle(img_hsv, (cX, cY), 10, (255, 0, 0), -1)
cv2.waitKey()

master_mask = sum(masks)
andRes = cv2.bitwise_and(img_hsv, img_hsv, mask=master_mask)
p0Res = cv2.bitwise_or(img_hsv, img_hsv, mask=masks[0])

