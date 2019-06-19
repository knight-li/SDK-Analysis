# -*- coding:utf-8 -*-
import os
import zipfile

# 操作路径
pathsour = 'D:\\My\\Python\\SDK-Analysis\\apk\\'
# baksmali.jar
baksmali = 'D:\\My\\Python\\SDK-Analysis\\baksmali.jar'
# 解析dex的基础命令
BaseToolCmd = 'java -jar baksmali.jar d '

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


# 修改文件后缀（将 .apk 修改为 .zip）
def changename(path):
  # 对目录下的文件进行遍历
  print(os.listdir(path))
  for file in os.listdir(path):
    # 判断是否是文件
    if os.path.isfile(os.path.join(path, file)):
      namelist = os.path.splitext(file)
      # 设置新文件名
      new_name = file.replace(file, '%s.zip' % namelist[0])
      print('new_name == %s' % new_name)
      # 重命名
      os.rename(os.path.join(path, file), os.path.join(path, new_name))


# 解压文件
def decompression(file, file_path, save_path):
  print(file_path, file)
  os.chdir(file_path)  # 转到路径
  r = zipfile.is_zipfile(file)  # 判断是否解压文件
  if r:
    zpfd = zipfile.ZipFile(file)  # 读取压缩文件
    pathtar = save_path + os.path.splitext(file)[0] + "\\"
    if os.path.exists(pathtar):
      print("文件夹存在")
    else:
      os.makedirs(pathtar)
      os.chdir(pathtar)  # 转到存储路径
      zpfd.extractall()
      zpfd.close()

    appName = os.path.splitext(file)[0]
    # 将 smali 拷贝到目录下
    if os.path.exists(pathtar + "baksmali.jar"):
      print("baksmali.jar 存在")
    else:
      copyBaksmaliToDir(pathtar)

    # 反编译
    decompileDex(pathtar, appName)


# 反编译解析 dex 文件
def decompileDex(Path, appName):
  os.chdir(Path)  # 切换到工作路径（必须要有）
  fileList = os.listdir(Path)
  for file_name in fileList:
    fname = os.path.splitext(file_name)[0]
    ftype = os.path.splitext(file_name)[1]
    if ftype == ".dex":
      print("找到dex 文件====> ", file_name)
      BaksmaliToolCmd = BaseToolCmd + file_name + ' -o ' + fname
      os.system(BaksmaliToolCmd)

      # 遍历查找 SDK 特征
      print("反编译完成====> ", Path + fname + "\\")
      checkSDKFeature(Path, fname, appName)


# 遍历查找 SDK 特征
def checkSDKFeature(Path, fname, appName):
  mPath = Path + fname + "\\"
  os.chdir(mPath)  # 切换到工作路径
  # 查找是否包含SDK
  searchSDK()

  os.chdir(Path)  # 完成之后切换到反编译路劲下


# 将baksmali 文件拷贝到要反编译的文件夹下
def copyBaksmaliToDir(pathtar):
  os.chdir(pathtar)
  cmdComand = "copy " + baksmali + " " + pathtar
  os.system(cmdComand)


# 查找 umengsdk
def searchUmengSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\UmengSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 友盟 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:

      apath = os.path.join(maindir, filename)
      if umengStr in apath or 'UMConfigure' in apath or 'MobclickAgent' in apath or "com\\umeng" in apath:
        print("umeng SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找极光 SDK
def searchJPushSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\JGSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 极光 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)

      str = None
      if JAnalyStr in apath:
        print("JAnalytic SDK ====> ", apath)
        str = '   JAnalytic SDK'
      elif JPushStr in apath or "libjpush" in apath:
        print("JPushStr SDK ====> ", apath)
        str = '   JPush SDK'
      elif JMessageStr in apath:
        print("JMessageStr SDK ====> ", apath)
        str = '   JMessage SDK'
      elif JShareStr in apath:
        print("JShareStr SDK ====> ", apath)
        str = '   JShare SDK'

      if str is not None:
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5] + str)
            fo.write('\n')
        except:
          pass


# 查找个推 SDK
def searchGeTuiSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\GeTuiSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 个推 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      str = None

      if GTStr in apath and GTStr_1 in apath or GTStr_2 in apath:
        print("个推 SDK ====> ", apath)
        str = '   个推 SDK'
      elif GSStr_1 in apath or GSStr_2 in apath:
        print("个数 SDK ====> ", apath)
        str = '   个数 SDK'
      elif GI in apath:
        print("个像 SDK ====> ", apath)
        str = '   个像 SDK'

      if str is not None:
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5] + str)
            fo.write('\n')
        except:
          pass


# 查找 MobSDK
def searchMobSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\MobSDKReport.txt"  # 保存文件路径
  strLine = "<================================ Mob SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if MobSDKStr in apath:
        print("Mob SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name  ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 TalkingData SDK
def searchTDSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\TDSDKReport.txt"  # 保存文件路径
  strLine = "<================================ TalkingData SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if TalkingDataStr in apath:
        print("talkingData SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 DU SDK
def searchDUSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\DUSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 数盟 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if DUSDKStr in apath:
        print("duSDKStr SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找数美 SDK
def searchSMSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\smSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 数美 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if SMSDKStr in apath or "libsmsdk.so" in apath or "shumei" in apath:
        print("smSDKStr SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找易观方舟 SDK
def searchYGSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\ygSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 易观方舟 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if YGSDKStr in apath:
        print("ygSDKStr SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找网易易盾 SDK
def searchWYSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\wySDKReport.txt"  # 保存文件路径
  strLine = "<================================ 网易易盾 SDK 集成情况 ================================>"
  try:
    with open(reportPath, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if WANGYIStr in apath:
        print("wangyiSDKStr SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 apk 所集成的 SDK
def searchSDK():
  searchUmengSDK()
  searchJPushSDK()
  searchTDSDK()
  searchTDSDK()
  searchYGSDK()
  searchDUSDK()
  searchSMSDK()
  searchMobSDK()
  searchWYSDK()


def main():
  global pathsour
  # 先改变后缀为.zip
  # changename(pathsour)
  # # 解压 .zip 文件
  # for filename in os.listdir(pathsour):
  #   decompression(filename, pathsour, pathsour)

  # 解压完后续需要查找是可将前面部分注释掉，只调用查找方法即可
  searchSDK()


if __name__ == '__main__':
  main()
