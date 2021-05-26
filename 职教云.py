import pymysql
import requests, json, time, smtplib, hashlib

sql_con = pymysql.connect(
    host='114.117.208.100',  # 数据库地址：本机地址为【localhost】；非本机地址填入第三方地址。
    port=3306,  # 端口号，数字类型，不加引号
    user='zhh',  # 用户名
    password='3zBTN2XwFnFySTWC',  # 数据库密码
    db='zhh',  # 数据库名
    charset='utf8')  # 数据库编码，一般为utf8)


def qb():
    cursor = sql_con.cursor()  # 链接数据库
    count = cursor.execute('select * from ZHH')
    sql_con.commit()
    for i in range(count):
        dqTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = cursor.fetchone()
        userName, userPwd = result[1], result[2]
        url_api = "https://zjyapp.icve.com.cn/newMobileAPI/"
        equipmentModel = "Xiaomi Redmi K20 Pro"
        equipmentApiVersion = 10
        try:
            equipmentAppVersion = getVersion()  # 如果   equipmentApiVersion=2.8.42 那么运行try处
        except:
            equipmentAppVersion = "2.8.45"
        emit = str(int(time.time())) + "000"
        basicData = {"equipmentAppVersion": equipmentAppVersion, "equipmentApiVersion": equipmentApiVersion,
                     "equipmentModel": equipmentModel}
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Host": "zjyapp.icve.com.cn",
                   "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/4.5.0", "emit": emit,
                   "device": getDevice(equipmentModel, str(equipmentApiVersion), equipmentAppVersion, emit)}
        userData = {"clientId": "bb702e1087904609a5de8dafe6241aa0", "sourceType": "2", "userPwd": userPwd,
                    "userName": userName,
                    "appVersion": equipmentAppVersion}
        userData.update(basicData)
        session = requests.Session()
        login = session.post(url_api + "MobileLogin/newSignIn", data=userData, headers=headers)
        loginInfo = json.loads(login.text)
        if loginInfo["code"] != 1:
            print("id是",result[0],userName, loginInfo["msg"])
        else:
            stuId = loginInfo["userId"]
            faceDate = (time.strftime("%Y-%m-%d", time.localtime()))
            newToken = loginInfo["newToken"]
            todayClassData = {"stuId": stuId, "faceDate": faceDate, "newToken": newToken}
            todayClassData.update(basicData)
            todayClass = session.post(url_api + "faceteach/getStuFaceTeachList", data=todayClassData, headers=headers)
            # 获取到签到的内容了
            todayClassInfo = json.loads(todayClass.text)["dataList"]
            result = ""
            # inClassData = {
            #     "activityId": todayClassInfo[i]["Id"], "stuId": stuId, "classState": todayClassInfo[i]["state"],
            #     "openClassId": todayClassInfo[i]["openClassId"],
            #     "newToken": newToken
            # }
            # 以下未调试
            for i in range(len(todayClassInfo)):  # 登录成功这里是循环两次
                inClassData = {
                    "activityId": todayClassInfo[i]["Id"], "stuId": stuId, "classState": todayClassInfo[i]["state"],
                    "openClassId": todayClassInfo[i]["openClassId"],
                    "newToken": newToken
                }
                inClassData.update(basicData)
                inClass = session.post(url_api + "faceteach/newGetStuFaceActivityList", data=inClassData,headers=headers)
                inClassInfo = json.loads(inClass.text)["dataList"]
                for n in range(len(inClassInfo)):
                    if inClassInfo[n]["DataType"] == "签到" and inClassInfo[n]["State"] != 3:  # 当
                        attendData = {
                            "activityId": todayClassInfo[i]["Id"], "openClassId": todayClassInfo[i]["openClassId"],
                            "stuId": stuId, "typeId": inClassInfo[n]["Id"], "type": "1",
                            "newToken": newToken
                        }
                        attendData.update(basicData)
                        attend = session.post(url_api + "faceteach/isJoinActivities", data=attendData, headers=headers)
                        attendInfo = json.loads(attend.text)
                        if attendInfo["isAttend"] != 1:
                            print("签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分")
                            print("签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分-签到部分")
                            signInData = {
                                "signId": inClassInfo[n]["Id"], "stuId": stuId,
                                "openClassId": todayClassInfo[i]["openClassId"], "sourceType": "2",
                                "checkInCode": inClassInfo[n]["Gesture"], "activityId": todayClassInfo[i]["Id"],
                                "newToken": newToken
                            }
                            print(signInData)
                            signInData.update(basicData)
                            signIn = session.post(url_api + "faceteach/saveStuSignNew", data=signInData,
                                                  headers=headers)
                            print(signIn)
                            signInInfo = json.loads(signIn.text)
                            print(signInInfo)
                            signInTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            print(signInTime)
                            print("这里会运行么")
                            result = result + (todayClassInfo[i]["courseName"] + " " + signInTime + " " + signInInfo[
                                "msg"]) + "\r\n"
                            print(result)
            if result == "":
                print(userName,"当前不存在未签到")
            else:
                # cursor.execute("INSERT INTO log VALUES('%s','%s') " % (zh, si))
                # sql_con.commit()
                print(result.replace("\r\n", " "))

def getVersion():
    versionInfo = requests.get("https://zjy2.icve.com.cn/portal/AppVersion/getLatestVersionInfo").json()
    return versionInfo["appVersionInfo"]["VersionCode"]
def getMd5(str):
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    return md5.hexdigest()
def getDevice(equipmentModel, equipmentApiVersion, equipmentAppVersion, emit):
    tmp = getMd5(equipmentModel) + equipmentApiVersion
    tmp = getMd5(tmp) + equipmentAppVersion
    tmp = getMd5(tmp) + emit
    return getMd5(tmp)
if __name__ == "__main__":
    while True:
        qb()
        time.sleep(0.001)