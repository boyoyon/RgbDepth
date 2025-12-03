import cv2, os, sys
import numpy as np
import open3d as o3d

delta = np.pi / 180
pcd = None

def key_callback_1(vis):

    angle = delta

    rotation = np.array([[np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def key_callback_2(vis):

    angle = -delta

    rotation = np.array([[np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def key_callback_3(vis):

    angle = delta

    rotation = np.array([[1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def key_callback_4(vis):

    angle = -delta

    rotation = np.array([[1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def key_callback_5(vis):

    angle = delta

    rotation = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def key_callback_6(vis):

    angle = -delta

    rotation = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)
    return True

def main():

    global pcd

    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print('%s displays point cloud using rgb_image and depth_image' % argv[0])
        print('[usage] python %s <rgb image> <depth image> [<zScale> <focal_length:x> <focal_length:y>]' % argv[0])
        quit()

    rgb = cv2.imread(argv[1])
    rgb = cv2.flip(rgb, 1)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    height, width = rgb.shape[:2]

    depth = cv2.imread(argv[2], cv2.IMREAD_UNCHANGED)
    depth = cv2.flip(depth, 1)

    h_depth, w_depth = depth.shape

    if h_depth != height or w_depth != width:
        depth = cv2.resize(depth, (width, height))

    fx = height
    fy = width

    zScale = 1.0

    if argc > 3:
        zScale = float(argv[3])
    
    if argc > 4:
        fx = int(argv[4])

    if argc > 5:
        fy = int(argv[5])

    cx = width // 2
    if argc > 6:
        cx = int(argv[6])

    cy = height // 2
    if argc > 7:
        cy = int(argv[7])

    print('zScale:%.1f, fx:%d, fy:%d, cx:%d, cy:%d' % (zScale, fx, fy, cx, cy))

    RGB = o3d.geometry.Image(rgb)

    #depth = 65535 - depth

    depth //= 2

    d_mean = int(np.mean(depth))

    depth += 30000 + d_mean

    DEPTH = o3d.geometry.Image(depth)
    
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            RGB, DEPTH, depth_scale=65535, convert_rgb_to_intensity=False)

    cam = o3d.camera.PinholeCameraIntrinsic()
    cam.intrinsic_matrix = np.asarray([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, cam)

    angle = np.arctan(width/height)
    cos = np.cos(-angle)
    sin = np.sin(-angle)

    #pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, zScale, 0], [0, 0, 0, 1]])
    #pcd.transform([[1, 0, 0, 0], [0, cos, -sin, 0], [0, sin, cos * zScale, 0], [0, 0, 0, 1]])

    pcd.transform([[1, 0, 0, 0], [0, cos, 0, 0], [0, 0, cos * zScale, 0], [0, 0, 0, 1]])

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.register_key_callback(ord("1"), key_callback_1)
    vis.register_key_callback(ord("2"), key_callback_2)
    vis.register_key_callback(ord("3"), key_callback_3)
    vis.register_key_callback(ord("4"), key_callback_4)
    vis.register_key_callback(ord("5"), key_callback_5)
    vis.register_key_callback(ord("6"), key_callback_6)

    # 実行
    vis.run()
    vis.destroy_window()

    # ply 書き出し
    # 時間が掛かるのでコメントアウト

    # base = os.path.basename(argv[1])
    # filename, _ = os.path.splitext(base)

    # dst_path = '%s_o3d.ply' % filename
    # o3d.io.write_point_cloud(dst_path, pcd)
    # print('save %s' % dst_path)

if __name__ == '__main__':
    main()
