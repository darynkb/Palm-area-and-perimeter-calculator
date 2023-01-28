# import sys

# sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np

data_file  = open("dataFile.txt", "w")

# Read the input image
name1 = "./resizedColored/P" 
name2 = 1
name3 = ".png"

for name2 in range(18):
    img = cv2.imread(name1+str(name2+1)+name3)
    data_file.write("Palm %d\r\n" % (name2+1))
    # Creating kernel
    kernel = np.ones((5, 5), np.uint8)
    # Using cv2.erode() method 
    img = cv2.erode(img, kernel)
    img = cv2.fastNlMeansDenoisingColored(img, None, 15, 8, 8, 15)

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

    # compute the area and perimeter
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        perimeter = round(perimeter, 4)
        print('#', i)
        print('Area:', area)
        print('Perimeter:', perimeter)
        data_file.write("# %d  " % (i))
        data_file.write("Area: %d  " % (area))
        data_file.write("Perimeter:%d " % (perimeter))
        if perimeter != 0:
            data_file.write("Ratio (area/perimeter):%d\r\n" % (area/perimeter))
        else:
            data_file.write("Ratio (area/perimeter): Division by zero\r\n")
        img1 = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
        x1, y1 = cnt[0,0]
        cv2.putText(img1, f'#{i}', (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(img1, f'Area:{area}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(img1, f'Perimeter:{perimeter}', (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # totalArea += area
        # totalPerim += perimeter
        filename = "./Area_Perimeter/P"+str(name2+1)+".png"
        cv2.imwrite(filename, img1)
        i = i + 1
    data_file.write("\r\n")

    cv2.imshow("Image"+str(name2+1), img)
    # print("Total area is ")
    # print(totalArea)
    # print("Total perimeter is ")
    # print(totalPerim)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
data_file.close()
