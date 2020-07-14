import cv2
import numpy as np

import sys
from PIL import Image
from io import BytesIO

def readimage(byteImg):
  stream = BytesIO(byteImg)
  return Image.open(stream).convert("RGBA")

def rectContour(contours):
  rects = []

  for i in contours:
    area = cv2.contourArea(i)
    if area > 50:
      peri = cv2.arcLength(i, True)
      approx = cv2.approxPolyDP(i, 0.02 * peri, True)
      if len(approx) == 4:
        rects.append(i)

  # return rects
  return sorted(rects, key=cv2.contourArea, reverse=True)

def getCornerPoints(contour):
  peri = cv2.arcLength(contour, True)
  approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

  return approx

def reorder(points):
  return np.array(sorted(points, key=lambda point: point.sum(1)))

def separateImageArea(originalImage, points, width, height):
  pt1 = np.float32(points)
  pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

  matrix = cv2.getPerspectiveTransform(pt1, pt2)
  img = cv2.warpPerspective(originalImage, matrix, (width, height))
  return img

def split(img, r = 1, c = 1):
  nr, nc = img.shape

  while nc % c != 0:
    nc += 1

  while nr % r != 0:
    nr += 1

  img = cv2.resize(img, (nc, nr))

  if r != 1:
    return np.vsplit(img, r)
  else:
    return np.hsplit(img, c)

def countWhitePoint(arr):
  return np.count_nonzero(arr == 255)

def crop(img):
  (x, y, w, h) = cv2.boundingRect(img)

  return img[y+30:y+h-20, x+70:x+w-50]