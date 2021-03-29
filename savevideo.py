# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:03:23 2020

@author: USER
"""
import skvideo
import pyrealsense2 as rs
import numpy as np
import cv2
import json
import torch
import skvideo.io
import os
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
size = (640, 480)
#save as avi
out = cv2.VideoWriter('color_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, size)
outdepth = cv2.VideoWriter('depth_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, size)
#or save as mp4
#out = cv2.VideoWriter('color_video.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)
#outdepth = cv2.VideoWriter('depth_video.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)
depth_numpy = []
color_numpy = []
all_depth_numpy = []
all_color_numpy = []
depth_fpath = "./numpy/depth.npy"
color_fpath = "./numpy/color.npy"
if os.path.exists(depth_fpath):
  os.remove(depth_fpath) # avoid keep append last time .npy file
if os.path.exists(color_fpath):
  os.remove(color_fpath) # avoid keep append last time .npy file

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

        ## save as numpy file
        depth_numpy = np.copy(depth_image)# avoid to change depth_image size while display video
        #depth_numpy = depth_image
        depth_numpy = np.expand_dims(depth_numpy, axis = 0) #change as n*480*640
        all_depth_numpy.append(depth_numpy) #list
        color_numpy = np.copy(color_image)# avoid to change color_image size while display video
        #color_numpy = color_image
        color_numpy = np.expand_dims(color_numpy, axis = 0) #change as n*480*640*3
        all_color_numpy.append(color_numpy) #list
        depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)

        # save video
        out.write(color_image)  
        outdepth.write(depth_image)
        #print(depth_image.shape)
        images = np.hstack((color_image, depth_image))
        cv2.imshow('window', images)
        key=cv2.waitKey(1)
        # stop and save image
        if key & 0xFF == ord('q') or key == 27:         
            out.release()
            outdepth.release()
            #cv2.imwrite('color_img.jpg', color_image)
            #cv2.imwrite('depth_img.jpg', depth_image) 
            print("depth: ",np.concatenate(all_depth_numpy,axis = 0).shape)
            print("color: ",np.concatenate(all_color_numpy,axis = 0).shape)
            np.save(depth_fpath, np.concatenate(all_depth_numpy,axis=0))
            np.save(color_fpath, np.concatenate(all_color_numpy,axis=0))

            break
   


finally:
    pipeline.stop()
