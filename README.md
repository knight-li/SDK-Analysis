# SDK-Analysis

## 前言

随着对 apk 内部集成 SDK 调研需求的增加，实现自动化检测 apk 包中 SDK 集成情况的功能是很有必要的。 因此，笔者创建了 SDK-Analysis 这个项目，目的就是自动化拆解 apk 包，并查找其是否集成所要了解的 SDK。

## 支持功能

目前支持 8 家 SDK 的检测：数盟，数美，极光，友盟，Mob，TalkingData，网易易盾，易观方舟；具体步骤：

- 解压 apk 文件
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
   reportPath = "D:\\MyProgects\\Python\SdkAnalysis\\logout\\UmengSDKReport.txt"
   ```

4. 总结要查找的 SDK 的特征值：

   ```Python
   # sdk feature
   umengStr = "com.umeng"
   JGuangStr = "JAnalyticsInterface"
   getuiStr = "getui"
   talkingDataStr = "TCAgent"
   MobSDKStr = "MobSDK"
   duSDKStr = "cn\shuzilm\core"
   smSDKStr = "SmAntiFraud"
   ygSDKStr = "AnalysysAgent"
   wangyiStr = "watchman"
   ```

至此，我们可以开启 apk 解析之旅了，启动项目。

## 输出文件

报告输出以 SDK 为单位，打印集成 SDK 的应用包名（下载后的apk名称），这样可以更方便的看到对应 SDK 都被哪些 apk 所集成。

项目中报告的路径如下：

![输入图片说明](https://images.gitee.com/uploads/images/2019/0618/160651_8e6448e3_5083058.png "19BFC349-7D7D-41af-B55B-9D6F585A1E8C.png")

以 DUSDKReport 为例，内部结构如下：

```
<=================== 数盟 SDK 集成情况 ===================>
app name ====> com.kuaikan.comic_5.40.0_540000
app name ====> com.kuaikan.comic_5.40.0_540000
app name ====> com.kuaikan.comic_5.40.0_540000
app name ====> com.kuaikan.comic_5.40.0_540000
```

可根据自身需求修改输出格式。

## 注意

- 由于  baksmali 在解包的时候速度会稍微慢一下，请耐心点;
- 由于解包后的文件比较大，记得及时清理

