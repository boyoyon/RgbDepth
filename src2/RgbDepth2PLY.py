# http://www.open3d.org/docs/latest/python_example/geometry/rgbd/index.html?highlight=pcd
import cv2, os, sys
import numpy as np
import open3d as o3d

delta = np.pi / 180
delta2 = 0.005

pcd = None

def key_callback_up(vis, action, mods):

    global delta, delta2

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:

        if ctrl_pressed:
            
            delta2 *= 1.5

        else:

            delta2 *= 1.1
    else:

        if ctrl_pressed:
            
            delta *= 1.5

        else:

            delta *= 1.1

    print(delta, delta2)

    return True

def key_callback_down(vis, action, mods):

    global delta, delta2

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:

        if ctrl_pressed:
            
            delta2 *= 0.5

        else:

            delta2 *= 0.9
    else:

        if ctrl_pressed:
            
            delta *= 0.5

        else:

            delta *= 0.9

    print(delta, delta2)

    return True

def key_callback_1(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_2(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_3(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    if ctrl_pressed:
        angle *= 10

    rotation = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_4(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, offset],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_5(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, offset],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_6(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0
    ctrl_pressed = (mods & 0x2) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    if ctrl_pressed:
        offset *= 10

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, offset],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def main():

    global pcd

    argv = sys.argv
    argc = len(argv)

    if argc < 3:
        print('%s loads ply and visualizes 3d model' % argv[0])
        print('%s <rgb image> <depth image> [<zScale> <focal_length:x> <focal_length:y>]' % argv[0])
        quit()

    rgb = cv2.imread(argv[1])
    #rgb = cv2.flip(rgb, 1)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    height, width = rgb.shape[:2]

    depth = cv2.imread(argv[2], cv2.IMREAD_UNCHANGED)
    #depth = cv2.flip(depth, 1)

    fx = width
    fy = height

    zScale = 1

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
    depth += 30000

    DEPTH = o3d.geometry.Image(depth)
    
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            RGB, DEPTH, depth_scale=65535, convert_rgb_to_intensity=False)

    cam = o3d.camera.PinholeCameraIntrinsic()
    cam.intrinsic_matrix = np.asarray([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, cam)

    center = pcd.get_center()
    pcd.translate(-center)

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.register_key_action_callback(ord("1"), key_callback_1)
    vis.register_key_action_callback(ord("2"), key_callback_2)
    vis.register_key_action_callback(ord("3"), key_callback_3)
    vis.register_key_action_callback(ord("4"), key_callback_4)
    vis.register_key_action_callback(ord("5"), key_callback_5)
    vis.register_key_action_callback(ord("6"), key_callback_6)
    vis.register_key_action_callback(ord("7"), key_callback_up)
    vis.register_key_action_callback(ord("8"), key_callback_down)

    # 実行
    vis.run()
    vis.destroy_window()

    if argc > 2:
        o3d.io.write_point_cloud('displayed.ply', pcd)
        print('save displayed.ply')

if __name__ == '__main__':
    main()
