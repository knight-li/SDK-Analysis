# SDK-Analysis

## 前言

随着对 apk 内部集成 SDK 调研需求的增加，实现自动化检测 apk 包中 SDK 集成情况的功能是很有必要的。 因此，笔者创建了 SDK-Analysis 这个项目，目的就是自动化拆解 apk 包，并查找其是否集成所要了解的 SDK。

## 支持功能

- 加压 apk 文件
- 通过 baksmali 解压 dex文件
- 查找 apk 中所需要的 SDK集成情况，并打印结果

## 基础使用
将代码下载到本地后：

1. 将要解析的 apk 放入项目的 apk 目录下，可以支持 n 个apk的解析工作

2. 根据自身情况修改文件路径，本示例以如下：

   ```Python
   # 要解析的 apk 文件路径
   pathsour = 'D:\\MyProgects\\Python\\SdkAnalysis\\apk\\'
   # baksmali.jar
   baksmali = 'D:\\MyProgects\\Python\\SdkAnalysis\\baksmali.jar'
   ```

3. 根据自身情况修改输出文件路径，本示例如下：

   ```Python
   filelistlog = "D:\\work\\DXSDKReport.txt"
   ```

至此，我们可以开启 apk 解析之旅了，启动项目。

## 输出文件

输出文件如下：

![输入图片说明](https://images.gitee.com/uploads/images/2019/0618/160651_8e6448e3_5083058.png "19BFC349-7D7D-41af-B55B-9D6F585A1E8C.png")

以 MobSDKReport 为例，内部结构如下：

```
<================================ SDK 集成情况 ================================>
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes\com\mob\MobSDK.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$1.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$2.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$3.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$4.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDKLog$1.smali
```

可根据自身需求修改输出格式。

## 注意

由于  baksmali 在解包的时候速度会稍微慢一下，请耐心点。
