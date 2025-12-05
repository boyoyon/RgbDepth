import os, sys, cv2
# import numpy as np
import copy

# keycode for cv2.waitKeyEx()
LEFT  = 2424832
UP    = 2490368
RIGHT = 2555904
DOWN  = 2621440

def callback(x):
    pass # do nothing

argv = sys.argv
argc = len(argv)

if(argc < 2):
    print('%s blurs the image with gaussian filter.' % argv[0])
    print('Usgae: >python %s <input image> [<output image>]' % argv[0])
    quit()

print('Hit ESC-key to terminate this program')

#img = cv2.imread(argv[1], cv2.IMREAD_COLOR)
#img = cv2.imread(argv[1], cv2.IMREAD_GRAYSCALE)
img = cv2.imread(argv[1], cv2.IMREAD_UNCHANGED)
H = img.shape[0]
W = img.shape[1]
out = copy.copy(img)

# create a window
cv2.namedWindow('image')

# create trackbar
cv2.createTrackbar('size', 'image', 1, 1000, callback)

SCALE = 1.0

pos = 1
prevPos = -1
prevScale = 1.0
fUpdate = True

print('Slide Trackbar or Press arrow-key to change gaussian blur size')
print('Press +/- to resize display image size')
print('Press ESC-key to terminate this program (blurred image is NOT saved)')
print('Press S-key to save blurred image and terminate this program')

clone = out.copy()

while(1):
    # retrieve the current position of trackbar
    pos = cv2.getTrackbarPos('size', 'image') 

    # blur with gaussian
    if pos != prevPos:
        size = pos * 2 + 1
        print('execute gaussian filter with the size %d' % size)
        out = cv2.GaussianBlur(img,(size, size), 0)
        prevPos = pos
        fUpdate = True

    if SCALE != prevScale or fUpdate:
 
        clone = cv2.resize(out, (int(W * SCALE), int(H * SCALE)))
        prevScale = SCALE
        fUpdate = True

    if fUpdate:
        cv2.imshow('image',clone)
        fUpdate = False

    key = cv2.waitKeyEx(100)
    if key == 27 or key == ord('S') or key == ord('s'):
        break

    elif key == RIGHT:
        pos += 1
    elif key == UP:
        pos += 3
    elif key == LEFT:
        pos -= 1
    elif key == DOWN:
        pos -= 3
    elif key == ord('+'):
        SCALE *= 1.1
    elif key == ord('-'):
        SCALE *= 0.9

    if pos < 0:
        pos = 0

    if pos > 1000:
        pos = 1000

    if pos != prevPos:
        cv2.setTrackbarPos('size', 'image', pos) 

if key == ord('S') or key == ord('s'):

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_gauss_%d.png' % (filename,size)
    cv2.imwrite(dst_path, out)
    print('save %s' % dst_path)

cv2.destroyAllWindows()
