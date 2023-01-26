# import sys

# sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np

# Read the input image
name1 = "./coloredSet/P" 
name2 = 18
name3 = ".png"
img = cv2.imread(name1+str(name2)+name3)

# Creating kernel
kernel = np.ones((5, 5), np.uint8)
# Using cv2.erode() method 
img = cv2.erode(img, kernel)
# img = cv2.fastNlMeansDenoisingColored(img, None, 15, 8, 8, 15)

# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding in the gray image to create a binary image
ret,thresh = cv2.threshold(gray,150,255,0)

# Find the contours using binary image
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of contours in image:",len(contours))
cnt = contours[0]
totalArea = 0
totalPerim = 0
i = 0
maxI = 0
maxArea = 0
maxPerimeter = 0

# compute the area and perimeter
for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    perimeter = round(perimeter, 4)
    print('Area:', area)
    print('Perimeter:', perimeter)
    img1 = cv2.drawContours(img, [cnt], -1, (255,190,220), 2)
    # x1, y1 = cnt[0,0]
    # cv2.putText(img1, f'Area:{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # cv2.putText(img1, f'Perimeter:{perimeter}', (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # totalArea += area
    # totalPerim += perimeter
    # if perimeter > maxPerimeter or area > maxArea : 
    #     maxI = i
    # i = i + 1

# cnt = contours[maxI]
# img1 = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
# x1, y1 = cnt[0,0]
# cv2.putText(img1, f'Area:{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
# cv2.putText(img1, f'Perimeter:{perimeter}', (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("Image", img)
filename = "./transparentImg/P"+str(name2)+".png"
cv2.imwrite(filename, img1)
# print("Total area is ")
# print(totalArea)
# print("Total perimeter is ")
# print(totalPerim)
cv2.waitKey(0)
cv2.destroyAllWindows()