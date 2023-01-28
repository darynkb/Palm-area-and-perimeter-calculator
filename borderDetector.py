# import sys

# sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np

# Read the input image
name1 = "./resizedColored/P" 
name2 = 1
name3 = ".png"
colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (100, 150, 169), (10, 220, 220)]

for name2 in range(18):
    img = cv2.imread(name1+str(name2+1)+name3)

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

    # compute the area and perimeter
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        perimeter = round(perimeter, 4)
        print('Area:', area)
        print('Perimeter:', perimeter)
        # print('CNT:', cnt)
        img1 = cv2.drawContours(img, [cnt], -1, colors[name2+1], 2) 

    cv2.imshow("Image", img)
    filename = "./resizedColored/P"+str(name2+1)+".png"
    cv2.imwrite(filename, img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()