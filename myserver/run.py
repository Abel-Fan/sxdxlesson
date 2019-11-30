from flask import Flask,render_template
import pymysql

app = Flask(__name__)

#连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',password='123456',
    database='sxlesson',
    charset='utf8')

@app.route("/")
def index():
    cursor = conn.cursor()
    sql = "select con from lessondata"
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    return render_template("index.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)