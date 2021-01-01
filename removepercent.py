import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
def removep(img_path,img_save):
	image = cv2.imread(img_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	# Morph open to remove noise
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
	kernel = np.ones((1,1),np.uint8)
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=100)

	# Find contours and remove small noise
	cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	for c in cnts:
	    area = cv2.contourArea(c)
	    if area < 80:
	        cv2.drawContours(opening, [c], -1, 0, -1)

	# Invert and apply slight Gaussian blur
	result = 255 - opening
	result = cv2.GaussianBlur(result, (3,3),0)
	cv2.imwrite(img_save,result)
	return img_save
	# cv2.imshow('thresh', thresh)
	# cv2.waitKey(0)
	# cv2.imshow('opening', opening)
	# cv2.waitKey(0)
	# cv2.imshow('result', result)
	# cv2.waitKey(0)
removep('blackbox.jpg','tryrem.jpg')