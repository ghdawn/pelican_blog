title: 记录写论文时用到的一些工具
date:2014-07-24 17:35:07
Tags:Python,计算机视觉
comments: true 
Category:Study

前一段时间，针对之前做过的关于目标跟踪的工作，我整理了一篇论文。论文中会需要一些实验图和数据曲线等，需要从算法的结果数据中生成，于是做了一些简单的小工具来批量生成数据，这里做个备忘，别以后忘掉了。主要用了一点ffmpeg，python和python的PIL库。

###从图像序列生成视频
假设当前目录下有一堆图像，命名分别为00001.pgm,00002.pgm.....，那么可以使用如下语句把他们变成视频。其中-r代表视频的帧率，越大图像越流畅越快，-i表示输入文件的命名格式，只要把文件名按照C语言的格式写就可以，(如我的就是%05d.pgm,如果文件名是pic1.png...pic10.png，那么可以用pic%d.png，以此类推)，最后加上文件名和扩展名就可以了。还有更复杂的命令，但是我用不到。
```shell
ffmpeg -r 24  -i %05d.pgm  test.mp4
```

效果如下视频：

<embed src="http://player.youku.com/player.php/sid/XNzA4MjI2OTM2/v.swf" allowFullScreen="true" quality="high" width="480" height="400" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash"></embed>

###跟踪结果与GT对比曲线
这里包括了我的算法，TLD，CT和MIL四种算法，分别与GT进行对比。对比数据包括了中心点误差和矩形框重合率
```python
from pylab import *

def Judge(truth,unknown):
    a=Overlap(truth,unknown)    
    b=Area(truth)
    c=Area(unknown)
    if a==0 or b==0 or c==0:
        return 0
    elif b+c-a>0:
        return float(a)/(c)
    else:
        return 0

def Correct(judge):
    return judge>0.5

def Area(sq):
    if isnan(sq[0]):
        return 0
    return (sq[3]-sq[1])*(sq[2]-sq[0])

def Overlap(A,B):
    if isnan(A[0]) or isnan(B[0]):
        return 0
    overlap=[]
    overlap.append(max(A[0],B[0]))
    overlap.append(max(A[1],B[1]))
    overlap.append(min(A[2],B[2]))
    overlap.append(min(A[3],B[3]))
    return Area(overlap)

def Center(A):
    a=[]
    a.append(A[1]+(A[3]-A[1])*0.5)
    a.append(A[0]+(A[2]-A[0])*0.5)
    return array(a)

def Distance(A,B):
    if isnan(A[0]) or isnan(B[0]):
        return 0
    a=Center(A)
    b=Center(B)
    c=square(a-b)
    return sqrt(c[0]+c[1])#/max(A[3]-A[1],(A[2]-A[0]))

dir='09_carchase'
print dir
gt=loadtxt(dir+'/gt.txt',delimiter=' ')

my=loadtxt('result_Mine/'+dir+'.txt')
tld=loadtxt('result_TLD/'+dir+'.txt',delimiter=',')
mil=loadtxt('result_MIL/'+dir+'.txt',delimiter=' ')
ct=loadtxt('result_CT/'+dir+'.txt',delimiter=' ')

minedis=sum([Distance(gt[i,:],my[i,:]) for i in range(0,len(my))])/len(my)
tlddis=sum([Distance(gt[i+1,:],tld[i,:]) for i in range(0,len(tld)-1)])/len(tld)
mildis=sum([Distance(gt[i,:],mil[i,:]) for i in range(0,len(mil))])/len(mil)
ctdis=sum([Distance(gt[i,:],ct[i,:]) for i in range(0,len(ct))])/len(ct)
print (minedis,tlddis,mildis,ctdis)
print '%d & %d & %d & %d \\' %(minedis,tlddis,mildis,ctdis)
```

###用多张小图生成一张大图
跟踪结果是一个图像的序列，论文里肯定不能全都贴上。可以在序列中抽取一些图像，组合一张大图做示意

```python
#coding=utf-8
import random,os
import Image,ImageFont,ImageDraw
import pylab

dir='my09_carchase'
imglength=224
row=2
col=5
font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf',20)
bigimg=Image.new('RGBA',(320*col,240*row))
dr=ImageDraw.Draw(bigimg)
height=0
imglist=[(imglength*i/(row*col)) for i in range (1,row*col+1)]
print (imglist)

for i in range(0,row*col):
    img=Image.open(dir+'/%05d.ppm' % imglist[i])
    img=img.convert('RGBA')
    draw=ImageDraw.Draw(img)
    draw.text((0,0),str(imglist[i]),font=font,fill='#ff0000')
    # dr.bitmap((320*((i-1)%5),height),img)
    bigimg.paste(img,(320*(i%col),240*(i/col)))
bigimg.save(dir+'.png')

```

### 从图像中提取出目标

在连续的跟踪过程中，会有一个矩形框跟随着目标，表示目标的位置。
```python
#coding=utf-8
import random,os
import Image,ImageFont,ImageDraw
import pylab

dir='09_carchase'
result=pylab.loadtxt('result_TLD/'+dir+'.txt',delimiter=',')
length=len(result)
width=result[0,2]-result[0,0]
height=result[0,3]-result[0,1]
for i in range(0,length):
    print i
    img=Image.open(dir+'/pgm/%05d.pgm' % (i+2))
    x0=int(result[i,0])
    y0=int(result[i,1])
    x1=x0+int(width)
    y1=y0+int(height)
    area=(x0,y0,x1,y1);
    roi=img.crop(area)
    dr=ImageDraw.Draw(img)
    roi.save('patch'+'/%05d.pgm'%i)
```