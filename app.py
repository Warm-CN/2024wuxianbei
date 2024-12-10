from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


@app.route('/guide')
def guide():
    return render_template("guide.html")


@app.route('/guide/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        team_name = request.form.get('team_name')
        captain_name = request.form.get('captain_name')
        number = request.form.get('number')
        tel = request.form.get('tel')
        academy = request.form.get('academy')
        my_class = request.form.get('class')
        teammate1_name = request.form.get('teammate1_name')
        teammate1_number = request.form.get('teammate1_number')
        academy1 = request.form.get('academy1')
        class1 = request.form.get('class1')
        teammate2_name = request.form.get('teammate2_name')
        teammate2_number = request.form.get('teammate2_number')
        academy2 = request.form.get('academy2')
        class2 = request.form.get('class2')

        print(team_name, captain_name, number, tel, academy, my_class, teammate1_name, teammate1_number, academy1,
              class1, teammate2_name, teammate2_number, academy2, class2)
        # 2.发送查询指令
        cursor.execute("select * from team where number = %s", [number, ])
        keys = cursor.fetchall()
        if keys:
            # 查找到数据发送修改数据指令
            cursor.execute(
                "update team set team_name = %s, captain = %s, number = %s, tel = %s, name1 = %s, number1 = %s, name2 = %s, number2 = %s,academy = %s,class=%s,academy1=%s,class1=%s,academy2=%s, class2=%s  where number = %s",
                [team_name, captain_name, number, tel, teammate1_name, teammate1_number, teammate2_name,
                 teammate2_number, academy, my_class, academy1, class1, academy2, class2, number, ])
            conn.commit()
        else:
            # 未查找到数据发送创建数据指令
            sql = "insert into team (team_name,captain,number,tel,name1,number1,name2,number2,academy,class,academy1,class1,academy2,class2) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, [team_name, captain_name, number, tel, teammate1_name, teammate1_number, teammate2_name,
                                 teammate2_number, academy, my_class, academy1, class1, academy2, class2, ])
            conn.commit()

        # 3.关闭
        cursor.close()
        conn.close()

        word = "报名成功！"
        return render_template("success.html", word=word)


@app.route('/guide/query', methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        return render_template("query.html")
    if request.method == 'POST':
        number = request.form.get('number')

        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.发送查询指令
        cursor.execute("select * from team where number = %s", [number, ])

        # 3.获取结果
        row = cursor.fetchone()

        # 3.关闭
        cursor.close()
        conn.close()

        word_list = ["队员1信息", "队员2信息", "姓名", "学号", "学院", "专业与班级"]
        flag = 1
        return render_template("return.html", word_list=word_list, row=row, flag=flag)


@app.route('/guide/query-acceptance', methods=['GET', 'POST'])
def query_acceptance():
    if request.method == 'GET':
        return render_template("query-acceptance.html")
    if request.method == 'POST':
        number = request.form.get('number')

        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.查询信息
        cursor.execute("select * from yanshou where number = %s", [number, ])
        row = cursor.fetchone()

        # 3.关闭
        cursor.close()
        conn.close()

        word_list = ["热身赛", "正赛", "时间", "地点"]
        return render_template("return.html", word_list=word_list, row=row)


@app.route('/guide/select-topic', methods=['GET', 'POST'])
def select_topic():
    if request.method == "GET":
        return render_template("select-topic.html")
    if request.method == "POST":
        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        topic = request.form.get('topic')
        number = request.form.get('number')

        # 发送查询指令
        cursor.execute("select * from team where number = %s", [number, ])
        keys = cursor.fetchall()

        flag = keys[0]['topic']

        if keys and flag != "B题":
            # 查找到数据发送修改数据指令
            cursor.execute(
                "update team set  topic = %s where number = %s",
                [topic, number, ])
            conn.commit()
            word = "选题成功！"
        elif flag == "B题":
            word = "无法修改选题！"
        else:
            word = "无信息！请先报名"

        # 3.关闭
        cursor.close()
        conn.close()

        return render_template("success.html", word=word)


@app.route('//form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        # ########## 从数据库获取所有用户信息 ###########
        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.发送指令
        sql = "select * from team"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        # 3.关闭
        cursor.close()
        conn.close()

        return render_template('form.html', data_list=data_list)
    if request.method == 'POST':
        # 1.连接MySQL
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="", charset='utf8', db='')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.获取输入内容
        condition = request.form.get("condition")
        data = request.form.get("data")

        # 3.判断筛选条件并进行查找
        if condition == "topic":
            cursor.execute("select * from team where topic = %s", [data, ])
            data_list = cursor.fetchall()

            # 关闭
            cursor.close()
            conn.close()

            return render_template('form.html', data_list=data_list)
        elif condition == "team":
            cursor.execute("select * from team where team_name = %s", [data, ])
            data_list = cursor.fetchall()

            # 关闭
            cursor.close()
            conn.close()

            return render_template('form.html', data_list=data_list)

        elif condition == "captain":
            cursor.execute("select * from team where captain = %s", [data, ])
            data_list = cursor.fetchall()

            # 关闭
            cursor.close()
            conn.close()

            return render_template('form.html', data_list=data_list)

        elif condition == "number":
            cursor.execute("select * from team where number = %s", [data, ])
            data_list = cursor.fetchall()

            # 关闭
            cursor.close()
            conn.close()

            return render_template('form.html', data_list=data_list)


if __name__ == '__main__':
    app.run(debug=True)
