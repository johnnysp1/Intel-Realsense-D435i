# Intel_realsense
## Goal
* RGB and depth realsense alignment calibration
* Save RGB and Depth video on real time
* Save numpy of video in depth and RGB
* Appearance ![alt tag](https://i.imgur.com/FBOGVIx.jpg)
## Environment setting
* Step 1: Add Intel server to the list of repositories :
```
$ echo 'deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main' | sudo tee /etc/apt/sources.list.d/realsense-public.list
```
* Step 2: Register the server’s public key :
```
$ sudo apt-key adv --keyserver keys.gnupg.net --recv-key 6F3EFCDE
```
* Step 3: Refresh the list of repositories and packages available
```
$ sudo apt-get update
```
* Step 4: In order to run demos install:
```
$ sudo apt-get install librealsense2-dkms
$ sudo apt-get install librealsense2-utils
```
* If you still encounter some error while running the codes, try to use `pip install` .

* Test: 
```
$ realsense-viewer
```
## Usage
* RGB and Depth Calibration: ```$ python 435di_align.py```
* Mixture of RGB and Depth image: 
```
$ mixture.py\
```
* Save RGB video + Depth video + RGB numpy file + depth numpy file : 
```
$ python savevideo.py
```
 and you can press ```q``` to quit 
* You can choose save the video into .mp4 or .avi format
## Demo
### Reference
