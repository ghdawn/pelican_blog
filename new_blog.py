#coding=utf-8
import time

print "Input filename"
name=" "
title="title:" + name+"\n";
date="date:"+ time.strftime('%Y-%m-%d %X',time.localtime())+"\n"
Tags="Tags:"
other="comments: true \nCategory:Study\n"
tags=[]
filename=raw_input()
filename=time.strftime('%Y-%m-%d-',time.localtime())+filename+".md"
tag=open('tags','r')
i=0
for t in tag:
	t=t[:-1]
	tags.append(t)
	print i,t
	i=i+1
N=raw_input()
N=N.split(' ')
for n in N:
	Tags+=tags[int(n)]
	Tags+=','
Tags=Tags[:-1]+'\n'
	
fout=open("content/"+filename,"w");
fout.write(title)
fout.write(date)
fout.write(Tags)
fout.write(other)
fout.close()