#!/usr/bin/python

import os
import subprocess
import sys

def Resample(filename,samprate):
    tempname=filename+'-temp'
    try:
        if(subprocess.check_output(['soxi','-r',filename]).rstrip() != str(samprate)):
            print "Converting: "+filename
            subprocess.call(['sox',filename,'-t','wav',tempname,'rate','-v',str(samprate)])
            subprocess.call(['mv','-f',tempname,filename])
            return True
    except subprocess.CalledProcessError:
        return False


def ScanDirectory(dir):
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
                if(Resample(dir+'/'+file,48000)):
                    print "SUCESS"

ScanDirectory(sys.argv[1])

