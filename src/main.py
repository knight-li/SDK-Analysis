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
umengStr = "com.umeng"
JGuangStr = "JAnalyticsInterface"
getuiStr = "getui"
talkingDataStr = "TCAgent"
MobSDKStr = "MobSDK"
duSDKStr = "cn\shuzilm\core"
smSDKStr = "SmAntiFraud"
ygSDKStr = "AnalysysAgent"
wangyiStr = "watchman"
dingXiangStr = "libDX"


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
  print(" checkSDKFuture ====> ", mPath)
  os.chdir(mPath)  # 切换到工作路径
  # 查找是否包含SDK
  searchSDK()

  os.chdir(Path)  # 完成之后切换到反编译路劲下


# 将baksmali 文件拷贝到要反编译的文件夹下
def copyBaksmaliToDir(pathtar):
  print(pathtar)
  os.chdir(pathtar)
  cmdComand = "copy " + baksmali + " " + pathtar
  print(cmdComand)
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
        print("filename ====> ", filename)
        print("umeng SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找极光 SDK
def searchJPushSDK():
  reportPath = "D:\\My\\Python\\SDK-Analysis\\logout\\JPushSDKReport.txt"  # 保存文件路径
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
      if JGuangStr in apath or "libjcore" in apath or "JPushInterface" in apath or "libjpush" in apath:
        print("JAnalytic SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name ====> " + apath.split('\\')[5])
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


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
      if getuiStr in apath:
        print("getui SDK ====> ", apath)
        try:
          with open(reportPath, 'a+') as fo:
            fo.writelines("app name  ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


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
      if talkingDataStr in apath:
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
    # print("maindir ====> ", maindir)
    # print("subdir ====> ", subdir)
    # print("file_name_list ====> ", file_name_list)
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      # if duSDKStr in apath or "libdu.so" in apath:
      if duSDKStr in apath:
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
      if smSDKStr in apath or "libsmsdk.so" in apath or "shumei" in apath:
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
      if ygSDKStr in apath:
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
      if wangyiStr in apath:
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
  changename(pathsour)
  # 解压 .zip 文件
  for filename in os.listdir(pathsour):
    decompression(filename, pathsour, pathsour)

  searchSDK()


if __name__ == '__main__':
  main()
