import cv2
from matplotlib import pyplot as plt
 
image = cv2.imread('../Image/Road_inverse_perspective.jpg')
 
height = image.shape[0]
width = image.shape[1]
 
cv2.line(image, (20,10), (100,10), (255,0,0), 2)
cv2.line(image, (0,0), (width, height), (0,0,255), 12)
 
plt.imshow(image)
plt.show()
    
