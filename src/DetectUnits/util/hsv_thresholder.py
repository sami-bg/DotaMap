# Credits to user nathancy on StackOverflow post 10948589
import cv2
import numpy as np
import scipy.ndimage

def nothing(x):
	pass

def thresholder(*supplemental, path=None, img=None):
	# Load image
	if not path:
		image = img
	elif not img:
		image = cv2.imread(path)
	# Create a window
	cv2.namedWindow('image')

	# Create trackbars for color change
	# Hue is from 0-179 for Opencv
	cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
	cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
	cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
	cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
	cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
	cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
	cv2.createTrackbar('contrast', 'image', 100, 300, nothing)
	cv2.createTrackbar('brightness', 'image', 0, 100, nothing)

	# Set default value for Max HSV trackbars
	cv2.setTrackbarPos('HMax', 'image', 179)
	cv2.setTrackbarPos('SMax', 'image', 255)
	cv2.setTrackbarPos('VMax', 'image', 255)

	# Initialize HSV min/max values
	hMin = sMin = vMin = hMax = sMax = vMax = 0
	phMin = psMin = pvMin = phMax = psMax = pvMax = 0

	while True:
		# Get current positions of all trackbars
		hMin = cv2.getTrackbarPos('HMin', 'image')
		sMin = cv2.getTrackbarPos('SMin', 'image')
		vMin = cv2.getTrackbarPos('VMin', 'image')
		hMax = cv2.getTrackbarPos('HMax', 'image')
		sMax = cv2.getTrackbarPos('SMax', 'image')
		vMax = cv2.getTrackbarPos('VMax', 'image')
		alpha = cv2.getTrackbarPos('contrast', 'image')
		beta = cv2.getTrackbarPos('brightness', 'image')

		# Set minimum and maximum HSV values to display
		lower = np.array([hMin, sMin, vMin])
		upper = np.array([hMax, sMax, vMax])

		# Convert to HSV format and color threshold
		# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		hsv = image
		adjusted = cv2.convertScaleAbs(image, alpha=(alpha/100), beta=beta)
		mask = cv2.inRange(adjusted, lower, upper)
		result = cv2.bitwise_and(adjusted, adjusted, mask=mask)

		# Print if there is a change in HSV value
		if (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax):
			print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
				hMin, sMin, vMin, hMax, sMax, vMax))
			phMin = hMin
			psMin = sMin
			pvMin = vMin
			phMax = hMax
			psMax = sMax
			pvMax = vMax

		# Display result image
		cv2.imshow('image', cv2.hconcat([result, *supplemental]))
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()
	return result
