from flask import Flask, request, render_template
import pymysql
import time
HTML_404="msg:请求错误,请联系管理员<a href='http://www.yonxi.cn' target='_blank'>小新</a>"
sql_con = pymysql.connect(host='114.117.208.100',  # 数据库地址：本机地址为【localhost】；非本机地址填入第三方地址。
                              port=3306,  # 端口号，数字类型，不加引号
                              user='zhh',  # 用户名
                              password='3zBTN2XwFnFySTWC',  # 数据库密码
                              db='zhh',  # 数据库名
                              charset='utf8')  # 数据库编码，一般为utf8)
cursor = sql_con.cursor()  # 链接数据库
#查好SELECT * FROM `ZHH` WHERE `账号` LIKE '1712203688'
#查密SELECT * FROM `ZHH` WHERE `密码` LIKE 'zyx123..'
# 查询账号密码SELECT * FROM `ZHH` WHERE `账号` LIKE '1712203688' AND `密码` LIKE 'zyx123..'
app=Flask(__name__)
@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception :
        return HTML_404
#登录区块
@app.route("/login",methods=["post"])
def login():
    try:
        name=request.form.get("dlname")
        mim=request.form.get("dlpass")
        cursor.execute("SELECT * FROM `ZHH` WHERE `账号` LIKE '%s' AND `密码` LIKE '%s'" % (name,mim))
        sql_con.commit()
        a = cursor.fetchone()
        if name == str(a[1]) or mim==str(a[2]):
            time1 = name, "于", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "请求登录"
            file = open("log.txt", "a")
            file.write(str(time1) + '\n')
            print(time1)
            return a[1]+"登录成功了"
    except Exception:
        #return "msg:提交错误,账号或密码错误<a href='http://127.0.0.1:5000/' target='_blank'>返回首页</a>'"
        return render_template("cwtz.html")
#注册区块
@app.route("/regist",methods=["post"])
def regist():
    try:
        name=request.form.get("zcname")
        mim=request.form.get("zcpass")
        cursor.execute("SELECT * FROM `ZHH` WHERE `账号` LIKE '%s'" % (name))
        sql_con.commit()
        b = cursor.fetchone()
        if name == b[1]:
            return render_template("cwtz.html")
    except Exception:
        cursor.execute("INSERT INTO ZHH VALUES (NULL, '%s', '%s')" % (name, mim))
        sql_con.commit()
        return name+"添加成功,从此解放双手吧,小新全程24h为你挂机服务!"

@app.route("/cx", methods=["post"])
def cx():
    try:
        name=request.form.get("cxname")
        count=cursor.execute("SELECT * FROM `log` WHERE `账号` LIKE '%s'" % (name))
        sql_con.commit()
        for i in range(count):
            result = cursor.fetchone()
            print(result)
            # openw = open("templates/log.txt", "w")
            # bl = name + " 于 " + result[1]
            # openw.write(bl + '\n')
        return str(result)
    except Exception:
        #return "msg:提交错误,账号或密码错误<a href='http://127.0.0.1:5000/' target='_blank'>返回首页</a>'"
        return "没有这个账号,或没有签到记录"
#错误提示
@app.route('/<name>')
def show(name):
        return HTML_404
if __name__ == "__main__":
    app.run(threaded=True)