import cv2, os, sys
import numpy as np

dither = np.array([[ 0,  8,  2, 10],
    [12,  4, 14,  6],[ 3, 11,  1,  9],[15,  7, 13,  5]])

argv = sys.argv
argc = len(argv)

print('%s converts heatmap image to depth image using dither' % argv[0])
print('[usage] python %s <headmap image>' % argv[0])

SPECTRAL = os.path.join(os.path.dirname(__file__), 'spectral.npy')
spectral = np.load(SPECTRAL)

nrSpectral = spectral.shape[0]

if spectral is None:
    print('Failed to load spectral')
    quit()

if argc < 2:
    quit()

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_depth_dither4x4.png' % filename

src = cv2.imread(argv[1])
H, W = src.shape[:2]

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

dst = np.empty((H, W, 1), np.float32)

# detect unique hues

hues = []

for y in range(H):
    for x in range(W):
        h = hsv[y][x][0]
        hues.append(h)

Hues = list(set(hues))

# create depth look-up table

Depths = []

for hue in Hues:

    minD = 255
    minI = -1

    for i in range(nrSpectral):

        d = np.abs(int(spectral[i]) - int(hue))
        if d == 0:
            Depths.append(i)
            break

        if d < minD:
            minD = d
            minI = i

    if d != 0:
        Depths.append(minI) 

# heatmap to depth

for y in range(H):
    print('processing %d/%d' % (y+1, H))

    for x in range(W):
        h = hsv[y][x][0]
        
        for i in range(len(Hues)):
            if h == Hues[i]:
                dst[y][x] = Depths[i] * 16 + dither[y % 4][x % 4]

dst *= 65535 / (nrSpectral * 31)
dst = np.clip(dst, 0, 65535)
dst = dst.astype(np.uint16)

cv2.imwrite(dst_path, dst)
print('save %s' % dst_path)
