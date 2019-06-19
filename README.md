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
   # 友盟
   umengStr = "com.umeng"
   
   # 极光
   JAnalyStr = "JAnalyticsInterface"  # 极光统计
   JPushStr = "JPushInterface"        # 极光推送
   JMessageStr = "JMessageClient"     # 极光IM
   JShareStr = "JShareInterface"      # 极光分享
   
   # 个推
   GTStr = "getui"
   GTStr_1 = "GTIntentService"
   GTStr_2 = "GetuiPushService"
   # 个数
   GSStr_1 = 'GsManager '
   GSStr_2 = 'GsConfig '
   # 个像
   GI = 'GInsightManager '
   
   # TalkingData
   TalkingDataStr = "TCAgent"
   # Mob
   MobSDKStr = "MobSDK"
   # 数盟
   DUSDKStr = "cn\shuzilm\core"
   # 数美
   SMSDKStr = "SmAntiFraud"
   # 易观方舟
   YGSDKStr = "AnalysysAgent"
   # 网易易盾
   WANGYIStr = "watchman"
   ```

***注意：***经分析，推送类 SDK 与大多数其他的分析类 SDK 不同，只是实现简单的发送和接受功能。而其他的sdk大多具备完整数据能力，因此对极光和个推的 SDK 类别做了区分。

至此，我们可以开启 apk 解析之旅了，启动项目。

## 输出文件

报告输出以 SDK 为单位，打印集成 SDK 的应用包名（下载后的apk名称），这样可以更方便的看到对应 SDK 都被哪些 apk 所集成。

项目中报告的路径如下：

 ![输入图片说明](https://images.gitee.com/uploads/images/2019/0619/164141_e2bcb265_5083058.png "6C659861-35C3-4dcc-887E-23CB42DD4B68.png")

以 JGSDKReport 为例，内部结构如下：

```
<========================== 极光 SDK 集成情况 ===========================>
app name ====> com.kuaikan.comic_5.40.0_540000   JPush SDK
app name ====> com.kuaikan.comic_5.40.0_540000   JAnalytic SDK
```

内容主要有APP名称，所集成的SDK名；可根据自身需求修改输出格式。

## 注意

- 由于  baksmali 在解包的时候速度会稍微慢一下，请耐心点;
- 由于解包后的文件比较大，记得及时清理

