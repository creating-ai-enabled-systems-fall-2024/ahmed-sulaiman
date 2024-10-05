import cv2
import numpy as np

def horizontal_flip(image):
    return cv2.flip(image, 1)

def gaussian_blur(image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(image, kernel_size, 0)

def resize(image, dimensions=(224, 224)):
    return cv2.resize(image, dimensions)

def rotate(image, angle):
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    return cv2.warpAffine(image, M, (w, h))

def brightness_adjust(image, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def crop(image, start_x, start_y, width, height):
    return image[start_y:start_y + height, start_x:start_x + width]