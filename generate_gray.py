import cv2
import sys
import numpy as np

if __name__ == '__main__':
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    gray = np.ones(shape=(height, width, 3), dtype=np.uint8) * 128
    cv2.imwrite('gray.jpg', gray)
