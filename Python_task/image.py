import numpy as np
import cv2


height = 1000
width = 1000
channels = 3 


image_array = np.random.randint(0, 256, size=(height, width, channels), dtype=np.uint8)
cv2.imshow('My 100x100 Image', image_array)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image displayed successfully. Press any key to close the window.")
