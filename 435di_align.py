# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:03:23 2020

@author: USER
"""
import pyrealsense2 as rs
import numpy as np
import cv2
import json
# import png
#!=====================================================================================================================
pipeline = rs.pipeline()

cfg = rs.config()
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 设定需要对齐的方式（这里是深度对齐彩色，彩色图不变，深度图变换）
align_to = rs.stream.color
# 设定需要对齐的方式（这里是彩色对齐深度，深度图不变，彩色图变换）
# align_to = rs.stream.depth

alignedFs = rs.align(align_to)
profile = pipeline.start(cfg)

try:
    while True:
        fs = pipeline.wait_for_frames()
        aligned_frames = alignedFs.process(fs)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame or not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)

        images = np.hstack((color_image, depth_image))
        cv2.imshow('window', images)
        key=cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.imwrite('color.jpg', color_image)
            cv2.imwrite('depth.jpg', depth_image) 
            break

finally:
    pipeline.stop()

