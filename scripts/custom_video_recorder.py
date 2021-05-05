#!/usr/bin/env python3

import cv2
import depthai as dai
import sys
import os

print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
# print(sys.argv[4])
# getting arguments which define the file names
video_number = sys.argv[1]

# getting arguments which decide the dimensions of the video
# video_height = int(sys.argv[2])
# video_width = int(sys.argv[3])
# video_frame_rate = float(sys.argv[4])

#Setting up the directory where we store the video
# path = os.getcwd()
# dir_name = video_number
# os.mkdir(dir_name)
# video_path = os.path.join(path,dir_name)
# os.chdir(path+"/"+dir_name)
# video_path_left = dir_name+"/"+video_file_name_left
# video_path_right = dir_name+"/"+video_file_name_right
# video_path_rgb = dir_name+"/"+video_file_name_rgb
# print(video_path_left)
# print(video_path_right)
# print(video_path_rgb)

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) cameras
camLeft = pipeline.createMonoCamera()
camLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
camLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

camRight = pipeline.createMonoCamera()
camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

camRgb = pipeline.createColorCamera()
camRgb.setPreviewSize(640, 400)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Create outputs
xoutLeft = pipeline.createXLinkOut()
xoutLeft.setStreamName('left')
camLeft.out.link(xoutLeft.input)

xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName('right')
camRight.out.link(xoutRight.input)

xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
camRgb.preview.link(xoutRgb.input)

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale frames from the outputs defined above
    qLeft = device.getOutputQueue(name="left", maxSize=1, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=1, blocking=False)
    qRGB = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)

    frameLeft = None
    frameRight = None
    frameRGB = None

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # videoLeft=cv2.VideoWriter(os.path.join(video_path,"left.mp4"),fourcc,video_frame_rate,(video_width,video_height),0)
    # videoRight=cv2.VideoWriter(os.path.join(video_path,"right.mp4"),fourcc,video_frame_rate,(video_width,video_height),0)
    # videoRGB=cv2.VideoWriter(os.path.join(video_path,"rgb.mp4"),fourcc,video_frame_rate,(video_width,video_height))
    videoLeft=cv2.VideoWriter(video_number+"_left.mp4",fourcc,30,(640,400),0)
    videoRight=cv2.VideoWriter(video_number+"_right.mp4",fourcc,30,(640,400),0)
    videoRGB=cv2.VideoWriter(video_number+"_rgb.mp4",fourcc,30,(640,400))

    while True:
        # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        inRGB = qRGB.tryGet()

        if inLeft is not None:
            frameLeft = inLeft.getCvFrame()

        if inRight is not None:
            frameRight = inRight.getCvFrame()

        if inRGB is not None:
            frameRGB = inRGB.getCvFrame()

        # show the frames if available
        if frameLeft is not None:
            cv2.imshow("left", frameLeft)
            #videoLeft.write(frameLeft)
            #print(frameLeft.shape)
        if frameRight is not None:
            cv2.imshow("right", frameRight)
            #videoRight.write(frameRight)
            #print(frameRight.shape)
        if frameRGB is not None:
            cv2.imshow("rgb", frameRGB)
            #videoRGB.write(frameRGB)
            #print(frameRGB.shape)
        if frameLeft is not None and frameRight is not None and frameRGB is not None:
            videoLeft.write(frameLeft)
            videoRight.write(frameRight)
            videoRGB.write(frameRGB)

        if cv2.waitKey(1) == ord('q'):
            videoRGB.release()
            videoLeft.release()
            videoRight.release()
            break
