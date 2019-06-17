# SDK-Analysis
这个工具主要是为了分析 apk 中所集成的 SDK 用的。
## 使用方法
1.将要查看的apk 放在工程里的 apk 目录下
2.将用于拆包的 baksmali.jar 放在工程的根目录下
3.指定输出log文件的地址，如‘D:\\My\\Python\\SdkAnalysis\\filelistlog.txt’
4.启动项目

## 输出文件示例

```
<==================SDK 集成情况 =========================>
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes\com\mob\MobSDK.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$1.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$2.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$3.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDK$4.smali
Mob SDK ====> D:\work\\JingpinAnalysis\apk\com.kuaikan.comic_5.40.0_540000\classes3\com\mob\MobSDKLog$1.smali
```
可根据自身需求修改输出格式。
