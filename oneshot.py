#! /usr/bin/env python

import theta_s_ctrl, time

cam = theta_s_ctrl.controller()

# confirm connection to Theta S
ret = cam.detect_camera()
print(ret)

# setup Theta S
cam.set_time('now')
cam.set_capturemode('single')
cam.set_mode('P')
cam.set_whitebalance('AUTO')
cam.set_expcomp(0)

# capture
cam.shutter()
time.sleep(2.0)

# file download
cam.download_latestfile('/home/pi/hogehoge.JPG')

# file SFTP to server
host = '192.168.100.255'
user = 'amigos'
passwd = raw_input()
local = '/home/pi/latest.JPG'
remote = '/Users/amigos/Pictures/testdir/latest.JPG'
cam.file_sftp(host, user, passwd, local, remote)

#file delete
cam.delete_latestfile()
