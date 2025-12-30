import cv2, os, sys
import numpy as np

def interpolate_lvl2(depthImage, X, D, y):

    for i in range(len(X)-1):

        x0 = X[i]
        x1 = X[i+1]

        d0 = D[i]
        d1 = D[i+1]

        depthImage[y][x0] = d0
        depthImage[y][x1] = d1

        Sign = 1
        DeltaY2 = (int(d1) - int(d0)) * 2
        if DeltaY2 < 0:
            Sign = -1
            DeltaY2 *= -1

        DeltaX  = x1 - x0
        DeltaX2 = DeltaX * 2

        Error = -DeltaX
        d = d0

        for x in range(x0+1, x1):

            Error += DeltaY2

            while Error > 0:
              d += Sign
              Error -= DeltaX2

            depthImage[y][x] = d

def interpolate(depth):

    H = depth.shape[0]
    W = depth.shape[1]

    d2 = np.zeros((H,W), np.uint16)

    for y in range(H):
    
        if y % 100 == 0:
            print('processing %d/%d' % (y, H))

        X = []
        D = []
    
        X.append(0)
        D.append(depth[y][0])
    
        for x in range(1, W):
    
            d = depth[y][x]
            if d != D[-1]:
                X.append(x)
                D.append(d)
    
        if len(X) < 2:
            d2[y,:]= X[0]
    
        else:
           interpolate_lvl2(d2,X,D,y)
    
        if X[-1] < W -1:
            interpolate_lvl2(d2, (X[-1], W-1), (D[-1], depth[y][W-1]), y)

    return d2

def main():

    blur_level = 8

    argv = sys.argv
    argc = len(argv)

    print('%s interpolates depth image' % argv[0])
    print('[usage] python %s <depth image> [<blur level(%d)>]' % (argv[0], blur_level))

    if argc < 2:
        quit()

    depth = cv2.imread(argv[1], cv2.IMREAD_UNCHANGED)

    if argc > 2:
        blur_level = int(argv[2])

    blur_size = blur_level * 2 + 1

    interpolated1 = interpolate(depth)

    cv2.imwrite('interpolated1.png', interpolated1)
    print('save interpolated1.png')

    rotCCWedDepth = cv2.rotate(depth, cv2.ROTATE_90_COUNTERCLOCKWISE)

    interpolated2 = interpolate(rotCCWedDepth)

    interpolated2 = cv2.rotate(interpolated2, cv2.ROTATE_90_CLOCKWISE)

    cv2.imwrite('interpolated2.png', interpolated2)
    print('save interpolated2.png')

    interpolated = (interpolated1.astype(np.int32) + interpolated2.astype(np.int32)) // 2

    interpolated = interpolated.astype(np.uint16)

    interpolated_and_blurred = cv2.GaussianBlur(interpolated,(blur_size, blur_size), 0)

    base = os.path.basename(argv[1])
    filename = os.path.splitext(base)[0]
    dst_path = '%s_interpolated_and_blurred_%d.png' % (filename, blur_level)

    cv2.imwrite(dst_path, interpolated_and_blurred)
    print('save %s' % dst_path)

if __name__ == '__main__':
    main()
