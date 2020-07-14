from flask import Flask, request, Response, render_template, redirect

import cv2
import numpy as np

from utils import rectContour, getCornerPoints, reorder, separateImageArea, split, readimage
from process import getExamIdValue, getStudentIdValue, getChoiceValue

app = Flask(__name__)

@app.route('/api/upload_image', methods=['POST'])
def main():
		if request.method == "POST":
			if request.files:
				binaryImage = request.files["image"].read()
				pil_img = readimage(binaryImage)
				img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
				
				SCALE_PERCENT = 40
				width = int(img.shape[1] * SCALE_PERCENT / 100)
				height = int(img.shape[0] * SCALE_PERCENT / 100)

				img = cv2.resize(img, (width, height))

				imgContours = img.copy()
				imgWithContourPoints = img.copy()

				imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
				imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
				imgCanny = cv2.Canny(imgBlur, 10, 50)

				contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
				cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 1)

				rects = rectContour(contours)

				firstChoiceAreaContour = getCornerPoints(rects[1])
				secondChoiceAreaContour = getCornerPoints(rects[0])
				studentIdContour = getCornerPoints(rects[4])
				examIdContour = getCornerPoints(rects[5])

				firstChoiceAreaContour = reorder(firstChoiceAreaContour)
				secondChoiceAreaContour =  reorder(secondChoiceAreaContour)
				studentIdContour = reorder(studentIdContour)
				examIdContour = reorder(examIdContour)

				firstChoiceAreaImage = separateImageArea(img, firstChoiceAreaContour, 175 *3, 455 * 3)
				secondChoiceAreaImage = separateImageArea(img, secondChoiceAreaContour, 175 * 3, 455 * 3)
				studentIdAreaImage = separateImageArea(img, studentIdContour, 80 * 2, 190 * 2)
				examIdAreaImage = separateImageArea(img, examIdContour, 40 * 5, 190 * 5)

				examIdGray = cv2.cvtColor(examIdAreaImage, cv2.COLOR_RGB2GRAY)
				examIdThresh = cv2.threshold(examIdGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

				studentIdGray = cv2.cvtColor(studentIdAreaImage, cv2.COLOR_RGB2GRAY)
				studentIdThresh = cv2.threshold(studentIdGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

				firstChoiceAreaGray = cv2.cvtColor(firstChoiceAreaImage, cv2.COLOR_RGB2GRAY)
				firstChoiceAreaThresh = cv2.threshold(firstChoiceAreaGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

				secondChoiceAreaGray = cv2.cvtColor(secondChoiceAreaImage, cv2.COLOR_RGB2GRAY)
				secondChoiceAreaThresh = cv2.threshold(secondChoiceAreaGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

				# result
				examId = getExamIdValue(examIdThresh)
				studentId = getStudentIdValue(studentIdThresh)
				studentChoices = getChoiceValue(firstChoiceAreaThresh) + getChoiceValue(secondChoiceAreaThresh)

				return {
					"examId": examId,
					"studentId": studentId,
					"values": studentChoices
				}
