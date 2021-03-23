import cv2
import numpy as np
img1 = cv2.imread('color.jpg' )
img = cv2.imread('depth.jpg' )
h, w, _ = img1.shape
# 函数要求两张图必须是同一个size
img2 = cv2.resize(img, (w,h), interpolation=cv2.INTER_AREA)
#print img1.shape, img2.shape
#alpha，beta，gamma可调
alpha = 0.5
beta = 1-alpha
gamma = 0
img_add = cv2.addWeighted(img1, alpha, img2, beta, gamma)
cv2.namedWindow('addImage')
cv2.imshow('img_add',img_add)
cv2.imwrite('align_mixture.jpg', img_add)
cv2.waitKey()
cv2.destroyAllWindows()
