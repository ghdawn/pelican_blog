#coding=utf-8
import time

print "Input Title"
name=raw_input()
title="title:" + name+"\n";
date="date:"+ time.strftime('%Y-%m-%d %X',time.localtime())+"\n"
other="comments: true \nTags:\nCategory:\n"

filename=raw_input()
filename=time.strftime('%Y-%m-%d-',time.localtime())+filename+".md"
fout=open("content/"+filename,"w");
fout.write(title)
fout.write(date)
fout.write(other)
fout.close()