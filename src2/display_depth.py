import os, sys, glob, cv2
from PIL import Image
import numpy as np
import copy

ESC = 27

mouse_x = -1
mouse_y = -1

l_button_down_x = -1
l_button_down_y = -1

def usage(progName):
    print('%s displays depth at the line of mouse position' % progName)
    print('%s <image file>' % progName)

def mouse_event(event, x, y, flags, param):
    global mouse_x, mouse_y, l_button_down_x, l_button_down_y
    mouse_x = x
    mouse_y = y
    
    if event == cv2.EVENT_LBUTTONDOWN:
        l_button_down_x = x
        l_button_down_y = y

def updateLineDepth(LineDepth, DepthImage, y):

    W = DepthImage.shape[1]

    cv2.rectangle(LineDepth, (0, 0), (W-1, 655), 255, -1)

    for x in range(W):
        d = DepthImage[y][x]
        yy = min(655, max(0, int(655 - d/100)))
        LineDepth[yy][x] = 0

    return 

def main():

    argv = sys.argv
    argc = len(argv)
    
    if(argc < 2):
        usage(argv[0])
        quit()
    
    DepthImage = cv2.imread(argv[1], cv2.IMREAD_UNCHANGED)
    H = DepthImage.shape[0]
    W = DepthImage.shape[1]
    
    cv2.imshow('depth_image', DepthImage)
    cv2.setMouseCallback('depth_image', mouse_event)
   
    scale = 1.0
    key = -1
    prev_mouse_x = -1
    prev_mouse_y = -1
    
    prev_l_button_down_x = -1
    prev_l_button_down_y = -1
    
    fUPDATE = False
    
    LineDepth = np.ones((656, W), np.uint8)
    
    while key != ESC:
        if fUPDATE or (mouse_x != prev_mouse_x) or (mouse_y != prev_mouse_y):
            ResizedDepthImage = cv2.resize(DepthImage, (int(W * scale), int(H * scale)))
            x = np.min((int(mouse_x / scale), W))
            y = np.min((int(mouse_y / scale), H))
           
            cv2.imshow('depth_image', ResizedDepthImage)
            prev_mouse_x = mouse_x
            prev_mouse_y = mouse_y
            fUPDATE = False
    
        if l_button_down_x != prev_l_button_down_x or l_button_down_y != prev_l_button_down_y:
            #x = np.min((int(mouse_x / scale), W))
            y = np.min((int(mouse_y / scale), H))
    
            updateLineDepth(LineDepth, DepthImage, y)
            ResizedLineDepth = cv2.resize(LineDepth, (int(W * scale), 656))
            cv2.imshow('Line_Depth', ResizedLineDepth)
    
            prev_l_button_down_x = l_button_down_x
            prev_l_button_down_y = l_button_down_y
            
        key = cv2.waitKey(10)
    
        if key == ord('-'):
            scale *= 0.9
            fUPDATE = True
    
        if key == ord('+'):
            scale *= 1.1
            fUPDATE = True
    
    cv2.destroyAllWindows()
    cv2.imwrite('line_depth.png', LineDepth)
    print('save line_depth.png')

if __name__ == '__main__':
    main()
