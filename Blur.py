#!/bin/python3

import argparse
import cv2
import  numpy as np

sizeZoom = []
locX = 0

'''
This dic use for size picture if input is wrong
'''
DEFAULT = {
    "x" : 400,
    "y" : 600,
}

'''
This def change str to num and if wrong set default
'''
def arg_to_num(size, x_or_y):
    true = True
    while true:
        if size.isnumeric():
            size = int(size)
            true = False
        else:
            size = DEFAULT[x_or_y]
            true = False

    return size

def click_and_crop(event, x, y, flags, param):
	global sizeZoom, locX

	if event == cv2.EVENT_LBUTTONDOWN:
		sizeZoom = [(x, y)]

	elif event == cv2.EVENT_LBUTTONUP:
		sizeZoom.append((x, y))
		locX = x

'''
get argument in terminal and set width and height and get size
'''
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-y", "--height", required=True, help="Please Enter a number for height")
ap.add_argument("-x", "--width", required=True, help="Please Enter a number for width")
args = vars(ap.parse_args())

'''
use input argument
'''
image = cv2.imread(args["image"])
sizeX = arg_to_num(args["height"], "x")
sizeY = arg_to_num(args["width"], "y")
image = cv2.resize(image, (sizeY, sizeX))#resize image by new size
clone = image.copy()
imageOrg = image.copy()
black = np.zeros((sizeX,sizeY,3), dtype="uint8")
black2 = black.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("e"):
        break

    if key == ord("r"):
        image = clone.copy()
        continue

    if locX > 0 :
        imageOrg = clone.copy()
        black = black2.copy()
        black = cv2.rectangle(black, (sizeZoom[0][0], sizeZoom[0][1]), (sizeZoom[1][0], sizeZoom[1][1]), (255,255,255), -1)
        mask = cv2.bitwise_and(imageOrg,black)
        mask = cv2.blur(mask, (5,5))
        imageOrg = cv2.rectangle(imageOrg, (sizeZoom[0][0], sizeZoom[0][1]), (sizeZoom[1][0], sizeZoom[1][1]), (0,0,0), -1)
        image = cv2.bitwise_or(mask, imageOrg)
        locX = 0

cv2.destroyAllWindows()