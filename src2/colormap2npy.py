import cv2
import numpy as np

src = cv2.imread('spectral.png')
H, W = src.shape[:2]

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

Hues = []

for y in range(H):
    for x in range(W):
        h = hsv[y][x][0]

        if not h in Hues:
            Hues.append(h)

hues = np.array(Hues)

np.save('spectral.npy', hues)
print('save spectral.npy')
print(hues)
print(hues.shape)
