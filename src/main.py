# -*- coding:utf-8 -*-
import os
import zipfile

# 操作路径
pathsour = 'D:\\work\\\JingpinAnalysis\\apk\\'
# baksmali.jar
baksmali = 'D:\\work\\ApkSignature\\baksmali.jar'
# 解析dex的基础命令
BaseToolCmd = 'java -jar baksmali.jar d '

# sdk feature
# 友盟
umengStr = "com.umeng"

# 极光
JAnalyStr = "JAnalyticsInterface"  # 极光统计
JPushStr = "JPushInterface"  # 极光推送
JMessageStr = "JMessageClient"  # 极光IM
JShareStr = "JShareInterface"  # 极光分享

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
tongdunStr = "libtongdun.so"

# 打开所有的日志文件
reportPath = "D:\\work\\JingpinAnalysis\\logout\\"


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
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if umengStr in apath or 'UMConfigure' in apath or 'MobclickAgent' in apath or "com\\umeng" in apath:
                print("umeng SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                print("app_name  ====> ", app_name)
                try:
                    with open(reportPath + 'UmengSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'UmengSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找极光 SDK
def searchJPushSDK():
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

            app_name = apath.split('\\')[5]
            if str is not None:
                try:
                    with open(reportPath + 'JGSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'JGSDKReport.txt', 'a+') as fo:
                                fo.writelines(str + " ====> " + app_name)
                                fo.write('\n')
                except:
                    pass


# 查找个推 SDK
def searchGeTuiSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            str = None

            if 'libgetuiext3.so' in apath or 'libgetuiext2.so' in apath or 'libgetuiext.so' in apath or 'com\igexin\sdk' in apath:
                print("个推 SDK ====> ", apath)
                str = '   个推 SDK '
            elif GSStr_1 in apath or GSStr_2 in apath:
                print("个数 SDK ====> ", apath)
                str = '   个数 SDK '
            elif GI in apath:
                print("个像 SDK ====> ", apath)
                str = '   个像 SDK '
            app_name = apath.split('\\')[5]
            if str is not None:
                try:
                    with open(reportPath + 'GeTuiSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'GeTuiSDKReport.txt', 'a+') as fo:
                                fo.writelines(str + "app_name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass


# 查找 MobSDK
def searchMobSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if MobSDKStr in apath:
                print("Mob SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'MobSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'MobSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name  ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找 TalkingData SDK
def searchTDSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if 'talkingdata' in apath or TalkingDataStr in apath:
                print("talkingData SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'TalkDSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'TalkDSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + apath.split('\\')[5])
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找 DU SDK
def searchDUSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if DUSDKStr in apath or "libdu.so" in apath:
                print("duSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'DUSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'DUSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找数美 SDK
def searchSMSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if SMSDKStr in apath or "libsmsdk.so" in apath or "shumei" in apath:
                print("smSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'SMSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'SMSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找易观方舟 SDK
def searchYGSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if 'AnalysysConfig' in apath or 'AnalysysAgent' in apath:
                print("ygSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'YGSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'YGSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找网易易盾 SDK
def searchWYSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if 'com\\netease\\mobsec\\rjsb' in apath or 'com\\netease\\mobsec\\rjsb\\watchman' in apath:
                print("wangyiSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'WYSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'WYSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找同盾 SDK
def searchTongDunSDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if "libtongdun.so" in apath:
                print("tongdun SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                try:
                    with open(reportPath + 'TongDSDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'TongDSDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + apath.split('\\')[5])
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找 MSA SDK
def searchMSASDK():
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:

            apath = os.path.join(maindir, filename)
            if "MiitHelper" in apath or "JLibrary" in apath \
                    or 'libA3AEECD8.so' in apath or 'lib37CF018B.so' in apath \
                    or "lib2D72A071.so" in apath or "lib34F225E9.so" in apath \
                    or "lib19282313.so" in apath or "lib423B8EB3.so" in apath:
                print("MAS SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                print("app_name  ====> ", app_name)
                try:
                    with open(reportPath + 'MSASDKReport.txt', 'r') as refo:
                        if app_name not in refo.read():
                            with open(reportPath + 'MSASDKReport.txt', 'a+') as fo:
                                fo.writelines("app name ====> " + app_name)
                                fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


# 查找 apk 所集成的 SDK
def searchSDK():
    # 查找指定 SDK 的集成情况
    # searchUmengSDK()
    # searchJPushSDK()
    # searchGeTuiSDK()
    # searchDUSDK()
    # searchSMSDK()
    # searchMobSDK()
    # searchWYSDK()
    # searchYGSDK()
    # searchTongDunSDK()
    # searchMSASDK()
    # searchTDSDK()

    # 查找所有 SDK集成情况
    str = None
    for maindir, subdir, file_name_list in os.walk(pathsour):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)

            # 1.友盟
            if umengStr in apath or 'UMConfigure' in apath or 'MobclickAgent' in apath or "com\\umeng" in apath:
                print("umeng SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('umeng', app_name)

            # 2.极光
            if JAnalyStr in apath:
                print("JAnalytic SDK ====> ", apath)
                str = 'JAnalytic SDK  ====> ' + apath.split('\\')[5]
                check_writeFile('JPush', str)
            if JPushStr in apath or "libjpush" in apath:
                print("JPushStr SDK ====> ", apath)
                str = 'JPushStr SDK ====> ' + apath.split('\\')[5]
                check_writeFile('JPush', str)
            if JMessageStr in apath:
                print("JMessageStr SDK ====> ", apath)
                str = 'JMessageStr SDK ====> ' + apath.split('\\')[5]
                check_writeFile('JPush', str)
            if JShareStr in apath:
                print("JShareStr SDK ====> ", apath)
                str = 'JShareStr SDK ====> ' + apath.split('\\')[5]
                check_writeFile('JPush', str)

            # 3.个推
            if 'libgetuiext3.so' in apath or 'libgetuiext2.so' in apath or 'libgetuiext.so' in apath or 'com\igexin\sdk' in apath:
                print("个推 SDK ====> ", apath)
                str = '个推 SDK ====> ' + apath.split('\\')[5]
                check_writeFile('getxin', str)
            if GSStr_1 in apath or GSStr_2 in apath:
                print("个数 SDK ====> ", apath)
                str = '个数 SDK ====> ' + apath.split('\\')[5]
                check_writeFile('getxin', str)
            if GI in apath:
                print("个像 SDK ====> ", apath)
                str = '个像 SDK ====>  ' + apath.split('\\')[5]
                check_writeFile('getxin', str)

            # 4.数盟
            if DUSDKStr in apath or "libdu.so" in apath:
                print("duSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('du', app_name)

            # 5.数美
            if SMSDKStr in apath or "libsmsdk.so" in apath or "shumei" in apath:
                print("smSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('shumei', app_name)

            # 6.Mob
            if MobSDKStr in apath:
                print("Mob SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('Mob', app_name)

            # 7.网易易盾
            if 'com\\netease\\mobsec\\rjsb' in apath or 'com\\netease\\mobsec\\rjsb\\watchman' in apath:
                print("wangyiSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('netease', app_name)

            # 8.易观方舟
            if 'AnalysysConfig' in apath or 'AnalysysAgent' in apath:
                print("ygSDKStr SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('ygSDKStr', app_name)

            # 9.同盾
            if "libtongdun.so" in apath:
                print("tongdun SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('tongdun', app_name)

            # 10. MSA
            if "MiitHelper" in apath or "JLibrary" in apath \
                    or 'libA3AEECD8.so' in apath or 'lib37CF018B.so' in apath \
                    or "lib2D72A071.so" in apath or "lib34F225E9.so" in apath \
                    or "lib19282313.so" in apath or "lib423B8EB3.so" in apath:
                print("MAS SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('MSA', app_name)

            # 11.TalkingData
            if 'com\\talkingdata\\sdk' in apath or TalkingDataStr in apath:
                print("talkingData SDK ====> ", apath)
                app_name = apath.split('\\')[5]
                check_writeFile('talkingdata', app_name)


# 检查并写入文件
def check_writeFile(type, app_name):
    if type == 'umeng':
        try:
            with open(reportPath + 'UmengSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'UmengSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'JPush':
        try:
            with open(reportPath + 'JGSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'JGSDKReport.txt', 'a+') as fo:
                        fo.writelines(app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'getxin':
        try:
            with open(reportPath + 'GeTuiSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'GeTuiSDKReport.txt', 'a+') as fo:
                        fo.writelines(app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'du':
        try:
            with open(reportPath + 'DUSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'DUSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'shumei':
        try:
            with open(reportPath + 'SMSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'SMSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)

    if type == 'Mob':
        try:
            with open(reportPath + 'MobSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'MobSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name  ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'netease':
        try:
            with open(reportPath + 'WYSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'WYSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'ygSDKStr':
        try:
            with open(reportPath + 'YGSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'YGSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'tongdun':
        try:
            with open(reportPath + 'TongDSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'TongDSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'MSA':
        try:
            with open(reportPath + 'MSASDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'MSASDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)
    if type == 'talkingdata':
        try:
            with open(reportPath + 'TalkDSDKReport.txt', 'r') as refo:
                if app_name not in refo.read():
                    with open(reportPath + 'TalkDSDKReport.txt', 'a+') as fo:
                        fo.writelines("app name ====> " + app_name)
                        fo.write('\n')
        except e as Exception:
            print('e======>\n' + e)


def initLogFiles():
    strLineUmeng = "<================================ 友盟 SDK 集成情况 ================================>"
    strLineJPush = "<================================ 极光 SDK 集成情况 ================================>"
    strLineTalkD = "<============================ TalkingData SDK 集成情况 ============================>"
    strLineYguan = "<============================== 易观方舟 SDK 集成情况 ===============================>"
    strLineDU = "<============================== 数字联盟 SDK 集成情况 ===============================>"
    strLineSM = "<================================ 数美 SDK 集成情况 ================================>"
    strLineMob = "<================================ Mob SDK 集成情况 ================================>"
    strLineWY = "<================================ 网易 SDK 集成情况 ================================>"
    strLineTongD = "<================================ 同盾 SDK 集成情况 ================================>"
    strLineMSA = "<================================ MSA SDK 集成情况 ================================>"
    strLineGT = "<================================ 个推 SDK 集成情况 ================================>"
    try:
        with open(reportPath + 'UmengSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineUmeng)
            fo.write('\n')

        with open(reportPath + 'JGSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineJPush)
            fo.write('\n')

        with open(reportPath + 'TalkDSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineTalkD)
            fo.write('\n')

        with open(reportPath + 'YGSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineYguan)
            fo.write('\n')

        with open(reportPath + 'DUSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineDU)
            fo.write('\n')

        with open(reportPath + 'SMSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineSM)
            fo.write('\n')

        with open(reportPath + 'MobSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineMob)
            fo.write('\n')

        with open(reportPath + 'WYSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineWY)
            fo.write('\n')

        with open(reportPath + 'TongDSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineTongD)
            fo.write('\n')

        with open(reportPath + 'MSASDKReport.txt', 'a+') as fo:
            fo.writelines(strLineMSA)
            fo.write('\n')

        with open(reportPath + 'GeTuiSDKReport.txt', 'a+') as fo:
            fo.writelines(strLineGT)
            fo.write('\n')
    except:
        pass  # 所以异常全部忽略即可


def main():
    global pathsour

    # 1.初始化日志文件
    initLogFiles()

    # 2.先改变后缀为.zip
    changename(pathsour)
    # 3.解压 .zip 文件
    for filename in os.listdir(pathsour):
        try:
            decompression(filename, pathsour, pathsour)
        except:
            pass

    # 解压完后续需要查找是可将前面部分注释掉，只调用查找方法即可
    # searchSDK()


if __name__ == '__main__':
    main()

