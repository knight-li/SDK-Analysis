# -*- coding:utf-8 -*-
import os
import zipfile

# 操作路径
# 设定文件路径
pathsour = 'D:\\MyProgects\\Python\\SdkAnalysis\\apk\\'
# baksmali.jar
baksmali = 'D:\\MyProgects\\Python\\SdkAnalysis\\baksmali.jar'
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
  # 遍历查找
  filelistlog = "D:\\My\\Python\\SdkAnalysis\\filelistlog.txt"  # 保存文件路径
  strLine = "<================================" + appName + "================================>"
  try:
    with open(filelistlog, 'a+') as fo:
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可

  for maindir, subdir, file_name_list in os.walk(pathsour + appName + "\\"):
    for filename in file_name_list:

      apath = os.path.join(maindir, filename)
      if umengStr in apath or 'UMConfigure' in apath or 'MobclickAgent' in apath:
        print("umeng SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines(apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可

      if JGuangStr in apath or "libjcore" in apath or "JPushInterface" in apath:
        print("JAnalytic SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines(apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可

      if getuiStr in apath:
        print("getui SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines(apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可
      if talkingDataStr in apath:
        print("talkingData SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines(apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可
      if MobSDKStr in apath or "com\mob\MobApplication":
        print("Mob SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines(apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可

  os.chdir(Path)  # 完成之后切换到反编译路劲下


# 将baksmali 文件拷贝到要反编译的文件夹下
def copyBaksmaliToDir(pathtar):
  print(pathtar)
  os.chdir(pathtar)
  cmdComand = "copy " + baksmali + " " + pathtar
  print(cmdComand)
  os.system(cmdComand)


# 已经解析过的文件，只遍历查找
def searchSDK():
  filelistlog = "D:\\work\\filelistlog.txt"  # 保存文件路径
  strLine = "<================================ SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:

      apath = os.path.join(maindir, filename)
      if umengStr in apath or 'UMConfigure' in apath or 'MobclickAgent' in apath:
        print("umeng SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("umeng SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可

      if JGuangStr in apath or "libjcore" in apath or "JPushInterface" in apath or "libjpush" in apath:
        print("JAnalytic SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("JAnalytic SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可

      if getuiStr in apath:
        print("getui SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("getui SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可
      if talkingDataStr in apath:
        print("talkingData SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("talkingData SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可
      if MobSDKStr in apath:
        print("Mob SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("Mob SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可
      if duSDKStr in apath or "libdu.so" in apath:
        print("duSDKStr SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("duSDKStr SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 umengsdk
def searchUmengSDK():
  filelistlog = "D:\\work\\UmengSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 友盟 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("umeng SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找极光 SDK
def searchJPushSDK():
  filelistlog = "D:\\work\\JPushSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 极光 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("JAnalytic SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找个推 SDK
def searchGeTuiSDK():
  filelistlog = "D:\\work\\GeTuiSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 个推 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("getui SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 MobSDK
def searchMobSDK():
  filelistlog = "D:\\work\\MobSDKReport.txt"  # 保存文件路径
  strLine = "<================================ Mob SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("Mob SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 TalkingData SDK
def searchTDSDK():
  filelistlog = "D:\\work\\TDSDKReport.txt"  # 保存文件路径
  strLine = "<================================ TalkingData SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("talkingData SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找 DU SDK
def searchDUSDK():
  filelistlog = "D:\\work\\DUSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 数盟 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("duSDKStr SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找数美 SDK
def searchSMSDK():
  filelistlog = "D:\\work\\smSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 数美 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("smSDKStr SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找易观方舟 SDK
def searchYGSDK():
  filelistlog = "D:\\work\\ygSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 易观方舟 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("ygSDKStr SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找网易易盾 SDK
def searchWYSDK():
  filelistlog = "D:\\work\\wySDKReport.txt"  # 保存文件路径
  strLine = "<================================ 网易易盾 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
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
          with open(filelistlog, 'a+') as fo:
            fo.writelines("wangyiSDKStr SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


# 查找顶象 SDK
def searchDXSDK():
  filelistlog = "D:\\work\\DXSDKReport.txt"  # 保存文件路径
  strLine = "<================================ 顶象 SDK 集成情况 ================================>"
  try:
    with open(filelistlog, 'a+') as fo:
      fo.write('\n')
      fo.write('\n')
      fo.writelines(strLine)
      fo.write('\n')
  except:
    pass  # 所以异常全部忽略即可
  for maindir, subdir, file_name_list in os.walk(pathsour):
    for filename in file_name_list:
      apath = os.path.join(maindir, filename)
      if "libDXCaptcha" in apath or "libDXRisk":
        print("DXSDKStr SDK ====> ", apath)
        try:
          with open(filelistlog, 'a+') as fo:
            fo.writelines("DXSDK SDK ====> " + apath)
            fo.write('\n')
        except:
          pass  # 所以异常全部忽略即可


def main():
  global pathsour
  # 先改变后缀为.zip
  changename(pathsour)
  # 解压 .zip 文件
  for filename in os.listdir(pathsour):
    decompression(filename, pathsour, pathsour)
  # 查找 apk 所集成的 SDK
  searchUmengSDK()
  searchJPushSDK()
  searchTDSDK()
  searchTDSDK()
  searchYGSDK()
  searchDUSDK()
  searchSMSDK()
  searchMobSDK()
  searchWYSDK()
  searchDXSDK()


if __name__ == '__main__':
  main()
