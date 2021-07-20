# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
import os
import time
import pdb


# def resize(im):
#     height = 147
#     width = 798
#     dim = (width, height)
#     return cv2.resize(im, dim)

# def remove_noise(im):
#     return cv2.medianBlur(im, 5)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to input image to be OCR'd")
ap.add_argument("-f", "--folder", required=True,
help="path to image folder")
ap.add_argument("-c", "--min-conf", type=int, default=0,
help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())

# totalTime = 0
totalconf = 0
for filename in os.listdir(args["folder"]):
	# load the input image, convert it from BGR to RGB channel ordering,
	# and use Tesseract to localize each area of text in the input image
	img = os.path.join(args["folder"], filename)
	im = cv2.imread(img)
	resized = cv2.resize(im, (1000, 200))
	#image = cv2.GaussianBlur(resized, (3,3), 0, 0)
	rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
	top = int(0.1*resized.shape[0])
	bottom = top
	left = int(0.1 * resized.shape[1])
	right = left
	dst = cv2.copyMakeBorder(rgb, top, bottom, left, right, cv2.BORDER_REPLICATE, None)
	# start = time.time()
	custom_config = r'-c tessedit_char_whitelist=QERTYUIOPASDGHJKLXCVBNM0123456789< --oem 3 --psm 6'
	results = pytesseract.image_to_boxes(dst, lang = None, config = custom_config, output_type=Output.DICT)
	print(results)
	# pdb.set_trace()
	# totalTime += (time.time()-start)
	# loop over each of the individual text localizations
	# for i in range(0, len(results["text"])):
	# 	# extract the bounding box coordinates of the text region from
	# 	# the current result
	# 	x = results["left"][i]
	# 	y = results["top"][i]
	# 	w = results["width"][i]
	# 	h = results["height"][i]
	# 	# extract the OCR text itself along with the confidence of the
	# 	# text localization
	# 	text = results["text"][i]
	# 	conf = int(results["conf"][i])
	# 	totalconf += conf
	# 	# filter out weak confidence text localizations
	# 	if conf >= args["min_conf"]:
	# 	# display the confidence and text to our terminal
	# 			print("Confidence: {}".format(conf))
	# 			print("Text: {}".format(text))
	# 			print("")
	# 	# 		# strip out non-ASCII text so we can draw the text on the image
	# 	# 		# using OpenCV, then draw a bounding box around the text along
	# 	# 		# with the text itself
	# 			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
	# 			cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# 			cv2.putText(dst, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
	# 				1.2, (0, 0, 255), 3)
	for i in range(0, len(results["char"])):
		x1 = results["left"][i]
		x2 = results["right"][i]
		y1 = results["top"][i]
		y2 = results["bottom"][i]
		char = results["char"][i]
		# print("Char: {}".format(char))
		cv2.rectangle(dst, (x1, y1), (x2, y2), (0, 255, 0), 2)
		# cv2.putText(dst, char, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
		# 			1.2, (0, 0, 255), 3)
	# show the output image
	cv2.imshow("Image", dst)
	if cv2.waitKey(0) & 0xFF == ord('q'): 
		break

#print(totalconf/200)
# print(totalTime/200)