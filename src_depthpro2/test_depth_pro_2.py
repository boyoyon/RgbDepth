import av
from depth_pro_2 import create_model_and_transforms, load_rgb, upright
import numpy as np
import cv2, os, sys

argv = sys.argv
argc = len(argv)

print('%s estimates depth from the image using depth_pro_2' % argv[0])
print('[usage] python %s <image>' % argv[0])

if argc < 2:
    quit()
 
model, transform = create_model_and_transforms("depthpro2-h")  # on the GPU if there is one

# A photo. f_px is the focal length recorded in the photo, or None.
image, f_px = load_rgb(argv[1])
depth = model.infer(transform(image), f_px=f_px)["depth"]  # meters, shape (height, width)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_depth.png' % filename


clipped = np.clip(depth.numpy(), 0, 10.0) * 65535 / 10
clipped = clipped.astype(np.uint16)

print(np.min(clipped), np.max(clipped))
cv2.imwrite(dst_path, clipped)
print('save %s' % dst_path)



