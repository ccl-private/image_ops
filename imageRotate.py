import cv2
from math import *

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, img = cap.read()

    # save (h, w) of the whole img
    height = img.shape[0]
    width = img.shape[1]

    # 输入任意角度
    angle = 90

    # compute the rotate matrix
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

    # comput the new (h, w) of the whole img after rotation
    heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
    widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))

    # fix the rotate matrix and rotate the whole img
    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))

    cv2.imshow("a", imgRotation)
    cv2.waitKey(1)
