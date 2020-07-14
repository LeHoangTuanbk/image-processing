import cv2
import numpy as np

from utils import split, countWhitePoint, crop

def getExamIdValue(img):
  cols = split(img, c= 3)

  result = []
  for col in cols:
    rows = split(col, r= 10)
    
    wp = []
    for row in rows:
      wp.append(countWhitePoint(row))

    result.append(wp.index(max(wp)))

  return result

def getStudentIdValue(img):
  cols = split(img, c= 6)

  result = []
  for col in cols:
    rows = split(col, r= 10)
    
    wp = []
    for row in rows:
      wp.append(countWhitePoint(row))

    result.append(wp.index(max(wp)))

  return result

def getChoiceValue(img):
  rows = split(img, r= 5)

  result = []

  for i, r in enumerate(rows):
    rows[i] = crop(r)
    
    subrows = split(rows[i], r=5)

    for sr in subrows:
      cols = split(sr, c=4)

      wp = []

      for col in cols:
          wp.append(countWhitePoint(col))

      ind = wp.index(max(wp))
      res = "A"
      if ind == 1:
        res = "B"
      if ind == 2:
        res = "C"
      if ind == 3:
        res = "D"

      result.append(res)
  return result
