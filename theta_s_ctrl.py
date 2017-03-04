#!/usr/bin/env python

import subprocess, time, datetime, paramiko

class controller:
    '''
    This program control RICOH THETA S camera.
    The controller class is powered by gphoto2 (http://gphoto.sourceforge.net/).
    This script is design for developers.
    Please use upper scripts, if you are a general user.
    '''

    def _send_gphoto2_(self, arg):
        cmd = 'sudo gphoto2 ' + arg
        subprocess.call(cmd, shell=True)
        return

    def _return_gphoto2_(self, arg):
        cmd = 'sudo gphoto2 ' + arg
        ret = subprocess.check_output(cmd, shell=True)
        return ret

    def detect_camera(self):
        ret = self._return_gphoto2_('--auto-detect')
        return ret

    def set_mode(self, mode='P'):
        if mode=='P':
            self._send_gphoto2_('--set-config expprogram=P')
        elif mode=='S':
            self._send_gphoto2_('--set-config expprogram=S')
        elif mode=='M':
            self._send_gphoto2_('--set-config expprogram=M')
        else:
            print('Cannot set mode = ' + mode)
            print('Only use P, S or M')
        return

    def query_mode(self):
        ret = self._return_gphoto2_('--get-config expprogram')
        if 'Current: P' in ret:
            mode = 'P'
        elif 'Current: S' in ret:
            mode = 'S'
        elif 'Current: M' in ret:
            mode = 'M'
        else:
            mode = 'unknown'
        return mode

    def set_time(self, clock='now'):
        if clock=='now':
            self._send_gphoto2_('--set-config datetime=now')
        else:
            tm = datetime.datetime.strptime(clock, '%Y%m%d%H%M%S')
            unix = int(time.mktime(tm.timetuple()))
            self._send_gphoto2_('--set-config datetime='+str(unix))
        return

    def query_time(self):
        ret = self._return_gphoto2_('--get-config datetime')
        ind = ret.find('Current:')
        unix = int(ret[ind+9:ind+19])
        systime = datetime.datetime.utcfromtimestamp(unix)
        utc = systime.strftime('%Y/%m/%d %H:%M:%S')
        return utc

    def query_battery(self):
        ret = self._return_gphoto2_('--get-config batterylevel')
        ind = ret.find('Current:')
        battery = str(ret[ind+9:ind+13])
        return battery

    def set_whitebalance(self, white='AUTO'):
        if white=='AUTO':
            self._send_gphoto2_('--set-config whitebalance=0')
        elif white=='SKY':
            self._send_gphoto2_('--set-config whitebalance=1')
        elif white=='LIGHT':
            self._send_gphoto2_('--set-config whitebalance=4')
        else:
            print('Cannot set  = ' + white)
            print('Only use AUTO, SKY or LIGHT')
        return

    def query_whitebalance(self):
        ret = self._return_gphoto2_('--get-config whitebalance')
        ind0 = ret.find('Current:')
        ind1 = ret.find('Choice: 0')
        ind2 = ret.find('Choice: 1')
        ind3 = ret.find('Choice: 4')
        wb = str(ret[ind0+9:ind0+15])
        if wb in ret[ind1+10:ind1+16]:
            white = 'AUTO'
        elif wb in ret[ind2+10:ind2+16]:
            white = 'SKY'
        elif wb in ret[ind3+10:ind3+16]:
            white = 'LIGHT'
        else:
            white = 'unknown'
        return white

    def set_expcomp(self, comp=0):
        complist = [-2, -1.7, -1.3, -1, -0.7, -0.3, 0, 0.3, 0.7, 1, 1.3, 1.7, 2]
        if comp in complist:
            self._send_gphoto2_('--set-config exposurecompensation='+str(comp))
        else:
            print('Cannot set = '+str(comp))
            print('Only use...')
            print(complist)
        return

    def query_expcomp(self):
        ret = self._return_gphoto2_('--get-config exposurecompensation')
        ind = ret.find('Current:')
        comp = float(ret[ind+9:ind+13])
        return comp

    def set_capturemode(self, mode='single'):
        if mode == 'single':
            self._send_gphoto2_('--set-config capturemode=0')
        elif mode == 'interval':
            self._send_gphoto2_('--set-config capturemode=1')
        else:
            print('Cannot set = '+str(mode))
            print('Only use single or interval')
        return

    def query_capturemode(self):
        ret = self._return_gphoto2_('--get-config capturemode')
        ind0 = ret.find('Current:')
        ind1 = ret.find('Choice: 0')
        ind2 = ret.find('Choice: 1')
        mode = str(ret[ind0+9:ind0+18])
        if mode in ret[ind1+10:ind1+19]:
            capmode = 'single'
        elif mode in ret[ind2+10:ind2+19]:
            capmode = 'interval'
        else:
            capmode = 'unknown'
        return capmode

    def set_capturedelay(self, delay=0):
        delaylist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        delay = int(delay)
        if delay in delaylist:
            self._send_gphoto2_('--set-config capturedelay='+str(delay))
        else:
            print('Cannot set = '+str(delay))
            print('Only use ...')
            print(delaylist)
        return

    def query_capturedelay(self):
        ret = self._return_gphoto2_('--get-config capturedelay')
        ind = ret.find('Current:')
        delay = int(ret[ind+9:ind+13])
        return delay

    def shutter(self):
        self._send_gphoto2_('--capture-image')
        return

    def download_latestfile(self, filepath='/home/pi/hoge.JPG'):
        ret = self._return_gphoto2_('--list-files')
        ind = ret.rfind('#')
        filenum = int(ret[ind+1:ind+5])
        self._send_gphoto2_('--get-file '+str(filenum)+' --filename='+filepath)
        return filepath

    def delete_latestfile(self):
        ret = self._return_gphoto2_('--list-files')
        sind = ret.rfind('R')
        eind = ret.rfind('JPG')
        filename = str(ret[sind:eind+3])
        self._send_gphoto2_('--delete-file /store_00010001/DCIM/100RICOH/'+filename)
        return filename

    def file_sftp(self, host, user, passwd, local, remote):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(host, username=user, password=passwd)
        sfconn = conn.open_sftp()
        sfconn.put(local, remote)
        sfconn.close()
        conn.close()
        return
#Written by K.Urushihara
