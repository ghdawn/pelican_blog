title: 关于ArDrone四旋翼 二次开发的一些记录
date:2014-03-31 13:51:23
Tags:Linux,Codes
comments: true 
Category:Study

AR.Drone是法国公司Parrot推出的四旋翼平台,内置飞控导航,摄像头等设备,可以使用各种手机,平板来控制飞行.同时官方提供了SDK,可以自己开发程序来控制该飞机.但是介绍总是美好的,在实际使用中总是会出现这样或那样的问题.这里我把遇到了的能解决并且能说得清楚的问题记录下来

使用的SDK版本为2.0.1,操作系统为64位ubuntu 13.04

##编译问题

刚解压出SDK,进入 *Example/Linux*,执行`make`命令,在编译**Navigation**工程时,会出现如下编译错误

     undefined reference to symbol 'floor@@GLIBC_2.2.5'

解决办法是在*Example/Linux/Navigation/Build/makefile*文件中的引用库的部分加入`-lm`,变成这样:
    
    GENERIC_LIBS+=-liw -lpc_ardrone -lgthread-2.0 -lgtk-x11-2.0 -lrt -lxml2 -ludev -lswscale -lSDL -lm
    
这样就可以通过编译了.
然后**video_demo**工程会出现下一个编译错误:

     undefined reference to symbol 'gdk_cairo_create'
     
其实这是一系列的编译错误,因为该工程的**makefile**里少加了很多引用库,于是同样的修改它的**makefile**,把引用的库变成这样:

    GENERIC_LIBS=-lpc_ardrone -lrt -lgtk-x11-2.0 -lcairo -lgdk-x11-2.0 -lgobject-2.0 -lm
    
这样就能通过编译了.
    
##开发中的问题

####读取不出高度信息

SDK中提供了和文档匹配的例程,其中**sdk_demo**是用来测试读取导航数据的.文档中说,所有单位都是千分之一的标准单位.即高度为*mm*,速度为*mm/s*,姿态为*1°/1000*.其中姿态信息可以正确的读出,而速度和高度的值一直是0.其中,读取高度的源码如下:

```c++
  inline C_RESULT demo_navdata_client_process( const navdata_unpacked_t* const navdata ) 
    {
        const navdata_demo_t*nd = &navdata->navdata_demo; 
        printf("Altitude      : %i\n",nd->altitude,);
        return C_OK;
    }
```

通过GDB调试,发现*navdata*中还有一个结构体叫**navdata_altitude**,其中有4个值:

1. altitude_vision
2. altitude_raw
3. altitude_ref
4. altitude_measure

后两个的读数不变恒为0.前两个的读数不为零,虽然不相等,但是很接近.当飞机对地面的距离变化时,可以看出变化趋势是正确的.通过名字可以推断,一个是通过底部摄像头的视觉算法估计高度,一个是通过底部的超声传感器的原始数据得到高度信息.所以使用如下代码,可以读出一个近似正确的高度信息.

这里我很奇怪,为什么官方提供的例程还不能很好的读取数值,还会出现这样的错误?

```C++
  inline C_RESULT demo_navdata_client_process( const navdata_unpacked_t* const navdata ) 
    {
        const navdata_demo_t*nd = &navdata->navdata_demo; 
        printf("Altitude      : %i\n",nd->altitude,); // get zero
        printf("Altitude      : %i %i\n",navdata->navdata_altitude.altitude_vision,navdata->navdata_altitude.altitude_raw); //sometimes get the number,and sometimes get zero
        return C_OK;
    
    }
```    

虽然通过这个结构体可以读取出来高度信息,但是这个信息并不稳定,运行一段时间就会都变成0.于是我找啊找啊,找到了一个感觉不太好的解决办法:

找到*ARDroneLIB/Soft/Lib/ardrone-tool/Navdata/ardrone_general_navdata.h*文件,把其中的第301行开始到305行结束的这一段**case**语句注释掉,就好了,如下.但是至于为什么这样就能好,我也还没搞清楚,以后再补充

```C++
case MULTICONFIG_REQUEST_NAVDATA:
      PRINTDBG ("Send application navdata demo/options");
      // Send application navdata demo/options to start navdatas from AR.Drone
      ARDRONE_TOOL_CONFIGURATION_ADDEVENT (navdata_demo, &ardrone_application_default_config.navdata_demo, NULL);
      ARDRONE_TOOL_CONFIGURATION_ADDEVENT (navdata_options, &ardrone_application_default_config.navdata_options, configurationCallback);
      configState = MULTICONFIG_IN_PROGRESS_NAVDATA;
      break;
```
