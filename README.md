# WeChat-Applet-Decrypt-Tools

## 0 简介

借助`Frida`导出`Windows`端微信小程序**未加密**源码的工具。

本项目源于[frida_with_wechat_applet](https://github.com/superdashu/frida_with_wechat_applet)，在使用过程中发现`frida_with_wechat_applet`无法获取到导出函数，经过测试修复后发布。

## 1 使用方法

1. 安装frida，`pip install frida`
2. `python3 find_applet.py`
3. 在微信设置中找到缓存目录，进入并删除所有`wx................`命名的文件夹
4. 打开目标小程序
5. 导出的包在`D://`中，也可以通过修改`line 29`的代码来指定路径

## 2 原理

`libruntime_host_export.dll`中有`EncryptBufToFile`函数，用于在获取到资源后加密并保存到本地。借助Frida对该函数进行Hook，当加载小程序时，该函数会被调用，从入参中即可获取到未加密的小程序数据。

原项目在拿到未加密的数据后覆盖加密后的文件，而本项目直接输出到指定路径中。



## 参考

[frida_with_wechat_applet](https://github.com/superdashu/frida_with_wechat_applet)
