#!/usr/bin/python

from __future__ import print_function

import ConfigParser
import mysql.connector
import os
import subprocess
import sys

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)


def Resample(filename,samprate):
    tempname=filename+'-temp'
    try:
        if(subprocess.check_output(['soxi','-r',filename]).rstrip() != str(samprate)):
            print("Converting: "+filename)
            subprocess.call(['rdconvert','--destination-format=0','--destination-file='+tempname,'--destination-sample-rate='+str(samprate),filename])
            subprocess.call(['mv','-f',tempname,filename])
            return True
    except subprocess.CalledProcessError:
        return False


def ScanDirectory(dir,rate):
    for file in os.listdir(dir):
        f0=file.split('.')
        f1=f0[0].split('_')
        if(len(f1)==2):
            try:
                cart=int(f1[0])
                cut=int(f1[1])
            except ValueError:
                cart=0;
                cut=0;
            if((cart>0)and(cart<1000000)and(cut>0)and(cut<1000)):
                if(Resample(dir+'/'+file,rate)):
                    sql='update CUTS set SAMPLE_RATE='+str(rate)
                    sql+=' where CUT_NAME="'+'{:06d}'.format(cart)+'_'+'{:03d}'.format(cut)+'"'
                    q=db.cursor()
                    q.execute(sql)

#
# Open the database
#
config=ConfigParser.ConfigParser()
config.readfp(open('/etc/rd.conf'))
db=mysql.connector.connect(user=config.get('mySQL','Loginname'),
                           password=config.get('mySQL','Password'),
                           host=config.get('mySQL','Hostname'),
                           database=config.get('mySQL','Database'))

if(len(sys.argv)!=2):
    eprint("rd_resample.py: missing samplerate argument")
    sys.exit(256)

if((int(sys.argv[1])!=32000) and 
   (int(sys.argv[1])!=44100) and 
   (int(sys.argv[1])!=48000)):
    eprint("rd_resample.py: invalid sample rate specified")
    sys.exit(256)

ScanDirectory('/var/snd',int(sys.argv[1]))

