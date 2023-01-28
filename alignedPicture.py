# import required library
import cv2
import numpy as np

x0 = 415    # Coordinates by which pictures will be centered(shifted).  
y0 = 570
diffX = 0
diffY = 0


# Read the input image
name1 = "./resizedColored/P" 
name2 = 1
name3 = ".png"
colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (67, 112, 255), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (100, 150, 169), (10, 220, 220)]


# function to display the coordinates of the points clicked on the image
def click_event_shiftPoint(event, x, y, flags, params):
    # checking for left mouse clicks
    global diffX
    global diffY
    if event == cv2.EVENT_LBUTTONDOWN:
        print('#',name2+1)
        print('Left Click: ShiftPoint')
        print(f'({x},{y})')
        # cv2.putText(img0, f'({x},{y})', (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # cv2.circle(img0, (x, y), 3, (0, 0, 255), -1)
        diffX = x0 - x
        diffY = y0 - y
        



def click_event_fingerPoint(event, x, y, flags, params):
   # checking for left mouse clicks
    global img0
    global img2
    global diffX
    global diffY
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Left Click: fingerPoint')
        print(f'({x},{y})')
        # cv2.putText(img0, f'({x},{y})', (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # cv2.circle(img0, (x, y), 3, (0, 0, 255), -1)

        # Creating kernel
        kernel = np.ones((5, 5), np.uint8)
            # Using cv2.erode() method 
        img2 = cv2.erode(img2, kernel)
            # img = cv2.fastNlMeansDenoisingColored(img, None, 15, 8, 8, 15)

            # convert the image to grayscale
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # Apply thresholding in the gray image to create a binary image
        ret,thresh = cv2.threshold(gray,150,255,0)

            # Find the contours using binary image
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) ##offset=(diffX,diffY)
        print("Number of contours in image:",len(contours))
        cnt = contours[0]

        diffAngle = 1.0 * np.rad2deg(np.arctan2(x-x0+diffX, y0-y-diffY))

        print("CalculationX: ", x-x0+diffX)
        print("CalculationY: ", y0-y+diffY)
        print("diffAngle: ", diffAngle)

            # Define the center of rotation
        center = (x0, y0)

            # Get the rotation matrix
        M = cv2.getRotationMatrix2D(center, diffAngle, 1.0)

            # Rotate the image
        img_rotated = cv2.warpAffine(img2, M, (img2.shape[1], img2.shape[0]))

            # Apply thresholding in the gray image to create a binary image
        gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,150,255,0)
            # Find the new contours
        contours_rotated, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(diffX,diffY))

        for cnt in contours_rotated: #45 80
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            perimeter = round(perimeter, 4)
            if (perimeter != 0 and area/perimeter > 45 and area/perimeter < 80):
                img0 = cv2.drawContours(img0, [cnt], -1, colors[name2], 2) 
        

# read the input image
img0 = cv2.imread('./resizedColored/P0.png')
for name2 in range(18):
      
    img2 = cv2.imread(name1+str(name2+1)+name3)

    gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    # Apply thresholding in the gray image to create a binary image
    ret,thresh = cv2.threshold(gray,150,255,0)

    # create a window
    cv2.namedWindow('Central shift Coordinates #'+str(name2+1))
    cv2.namedWindow('Middle finger Coordinates #'+str(name2+1))

    # bind the callback function to window
    cv2.setMouseCallback('Central shift Coordinates #'+str(name2+1), click_event_shiftPoint)
    cv2.setMouseCallback('Middle finger Coordinates #'+str(name2+1), click_event_fingerPoint)

    while True:
        cv2.imshow('Central shift Coordinates #'+str(name2+1), img2)
        k = cv2.waitKey(1) & 0xFF
        if k == 32:
            break
    cv2.destroyWindow('Central shift Coordinates #'+str(name2+1))

    while True:
        cv2.imshow('Middle finger Coordinates #'+str(name2+1), img2)
        k = cv2.waitKey(1) & 0xFF
        if k == 32:
            break
    cv2.destroyWindow('Middle finger Coordinates #'+str(name2+1))


cv2.namedWindow('Result')
cv2.imshow('Result', img0)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the result image
filename = "./ResultPicture/result.png"
cv2.imwrite(filename, img0)