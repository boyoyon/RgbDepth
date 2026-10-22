from ultralytics import YOLO
import numpy as np
import cv2, os, sys

argv = sys.argv
argc = len(argv)

print('%s estimates depths of objects in the image' % argv[0])
print('[usage] python %s <image>' % argv[0])

if argc < 2:
    quit()

model = YOLO(os.path.join(os.path.dirname(__file__), 'yolo26n-depth.pt'))
results = model(argv[1])
 
# Dense metric depth: a (H, W) float array, meters per pixel
depth = results[0].depth.data.cpu().numpy()

dmax = np.max(depth)
depth *= 65535 / dmax
depth = np.clip(depth, 0, 65535)
depth = depth.astype(np.uint16)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_depth.png' % filename

cv2.imwrite(dst_path, depth)
print('save %s' % dst_path)
