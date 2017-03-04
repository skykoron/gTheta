#! /usr/bin/env python

import theta_s_ctrl, time, signal, datetime, os

signal.signal(signal.SIGINT, signal.SIG_DFL)
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

# setup SFTP server
host = '192.168.100.235'
user = 'amigos'
passwd = 'NakaY0s1'
fname_from_theta = '/home/pi/latest.JPG'
interval = 2 #min

# capture loop
while 1:
    cam.shutter()
    time.sleep(2.0)

    # file download
    cam.download_latestfile(fname_from_theta)

    # file SFTP to server
    t = datetime.datetime.now()
    ut = t.strftime('%Y%m%d_%H%M%S')
    remote = '/Users/amigos/Pictures/testdir/Nagoya_'+ut+'.JPG'
    cam.file_sftp(host, user, passwd, fname_from_theta, remote)

    #file delete
    cam.delete_latestfile()
    os.remove(fname_from_theta)

    # sleep time
    for i in range(interval):
        ret = cam.query_battery
        print('interval: '+str(i)+' min')
        time.sleep(60)

