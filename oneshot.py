#! /usr/bin/env python

from PIL import Image
import theta_s_ctrl, time

cam = theta_s_ctrl.controller()

ret = cam.detect_camera()
print(ret)

cam.set_time('now')


cam.set_capturemode('single')
cam.set_mode('P')
cam.set_whitebalance('AUTO')
cam.set_expcomp(0)

cam.shutter()

time.sleep(2.0)

cam.download_latestfile('/home/pi/hogehoge.JPG')

img = Image.open('/home/pi/hogehoge.JPG')
img.show()

