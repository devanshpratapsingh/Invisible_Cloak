#importing libraries
import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0) #you can change this according to your choice of camera, my initial webcam is 0 

time.sleep(3)

background = 0
count = 0

#capturing background
for i in range(30):
    ret,background = cap.read()
background = np.flip(background, axis=1)

while(cap.isOpened()):

    ret, img = cap.read()
    if not ret:
        break

    count += 1
    img = np.flip(img, axis=1)

    #HSV value
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,120,70])
    upper_red = np.array([10, 255, 255])
    #Mask wala segment is sepetaring the cloak part
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2 #OR 1 or x

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations=2) #Morph open is used to remove noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)#Morph Dilate is used for smoothness

    mask2 = cv2.bitwise_not(mask1)
    #Mask 1 was seperating the cloak, and Mask2 is opposite of Mask1 so it has everything eccept the cloak

    result1 = cv2.bitwise_and(background, background, mask= mask1)#Used for segmentation of colour, i.e. differentiating cloak color with the background color
    result2 = cv2.bitwise_and(img, img, mask=mask2)# Used to substitute the cloak part
    final_output = cv2.addWeighted(result1, 1, result2, 1, 0)

    cv2.imshow('Avada Kedavra🎇✨', final_output)
    k = cv2.waitKey(10)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()



