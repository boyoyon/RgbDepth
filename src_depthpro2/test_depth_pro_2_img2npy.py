import av
from depth_pro_2 import create_model_and_transforms, load_rgb, upright
import numpy as np
import glob, os, sys

argv = sys.argv
argc = len(argv)

print('%s estimates depth from the image using depth_pro_2' % argv[0])
print('[usage] python %s <wildcard for images>' % argv[0])
print('[usage] python %s <image1> <image2> <image3> ...' % argv[0])

if argc < 2:
    quit()
 
model, transform = create_model_and_transforms("depthpro2-h")  # on the GPU if there is one

paths = []

if argc > 2:
    for i in range(1, argc):
        paths.append(argv[i])

else:
    paths = glob.glob(argv[1])

for p in paths:

    # A photo. f_px is the focal length recorded in the photo, or None.
    image, f_px = load_rgb(p)
    depth = model.infer(transform(image), f_px=f_px)["depth"]  # meters, shape    (height, width)

    base = os.path.basename(p)
    filename = os.path.splitext(base)[0]
    dst_path = '%s_depth.npy' % filename

    no = 2
    while os.path.exists(dst_path):
        dst_path = '%s_depth_%d.npy' % (filename, no)
        no += 1

    np.save(dst_path, depth)
    print('save %s' % dst_path)



