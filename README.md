# Py3D

A simple 3D engine based on python, including a 3D model viewer and a 3D function image rendering tool.

基于 Python 实现的简易 3D 引擎，包括一个 3D 模型查看器与一个三维函数图像绘制工具。（各提供使用 [tkinter](frontends/tkinter) 和 [PyQt5](frontends/qt) 实现的两种版本）

![screenshot](/screenshots/screenshot.gif)

## Operation

| Operation | Usage |
| --- | --- |
| Left button | Rotate the view. |
| Middle button | Move the camera. |
| Right button | Rotate the screen. |
| Mouse wheel | Move forward/backward. |

## ObjV3D

A simple 3D model viewer that supports reading .obj format files.

一个简单的 3D 模型查看器，支持读取 .obj 格式文件

![screenshot](/screenshots/obj_viewer.png)

### Usage

```sh
python3 -m Py3D.frontends.{tkinter/qt}.obj_viewer assets/teapot.obj
```

## Plot3D

A 3D function image rendering tool.

一个三维函数图像绘制工具。

![screenshot](/screenshots/plot3d.png)

### Usage

```sh
python3 -m Py3D.frontends.{tkinter/qt}.plot3d
```
