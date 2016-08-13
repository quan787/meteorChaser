# meteorChaser

[meteor.bnuastro.club](http://meteor.bnuastro.club/) 流星监控数据的存储和管理
欢迎加入我们

## 依赖软件
*	wamp
*	python2.7
*	ffmpeg
*	(python模块)VideoCapture
*	(python模块)pywin32
*	(python模块)pymysql
*	(js插件)Echarts

## 数据库结构
数据库名：meteorchaser
表：webmeteor

*	id int(11) a_i
*	date varchar(10)
*	name varchar(40)
*	type int(8)

表：weather

*	hour varchar(10)
*	temperature float
*	skycon varchar(20)
*	cloudrate float
*	aqi float
*	humidity float
*	pm25 float
*	intensity float

表：rawdata

*		请按照UFOAnalyzer软件数据文件进行导入

## 文件系统

*	UFOCapture文件存储目录：C:\meteor\
*	永久存储目录：D:\meteor\
*	转码视频目录：D:\meteor\recoded\

## 简介

本系统使用高灵敏度的CCD监控摄像头，配合UFOCapture软件进行流星监测。

装置介绍：[meteor.bnuastro.club/detail.html](http://meteor.bnuastro.club/detail.html)

文件存储地址：[meteor.bnuastro.club/file/](http://meteor.bnuastro.club/file/)

gihub链接：[meteorChaser](https://github.com/quan787/meteorChaser)

## 目标功能

*   定时对新的视频文件进行转码，以适合网络播放（已完成）
*   流星图片和视频的在线展示，进行证认和分类（已完成）
*   建立流星数据库（已完成）
*	观测数据统计图（已完成）
*   对热门的流星可以提交评论、目击报告等。（待填）
![装置图片](http://meteor.bnuastro.club/pic/IMG_1484.JPG)
![流星](http://meteor.bnuastro.club/pic/meteor1.gif)
