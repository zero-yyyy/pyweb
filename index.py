from flask import *
from server_conf import *
from fun import *

app = Flask(__name__, static_folder='static')
app.secret_key = '202212090068lzy'


# 初始界面 index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# 注册界面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 检查用户名是否已存在
        if is_username_taken(username):
            return "<script>alert('用户名已存在，请选择其他用户名！'); window.location.href = '/register';</script>"
        else:
            # 注册用户并写入数据库
            register_user(username, password)
            return "<script>alert('注册成功！'); window.location.href = '/login';</script>"
        
    return redirect(url_for('index'))  # 重定向到主页或其他已定义的路由

# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 调用登录验证函数
        if login_auth('users', username, password):
            # 验证成功，将用户信息存储在会话中
            session['user'] = {
                'username': username,
                'password': password,  # 示例邮箱
                'role': 0,
                'loginstatus': 1,
            }
            return redirect(url_for('user_login'))
        else:
            # 验证失败，返回错误信息或重定向到登录页面
            return "<script>alert('用户名或者密码错误，请重新登录！'); window.location.href = '/login';</script>"
        
# 用户登录成功后的页面
@app.route('/user/userlogin')
def user_login():
    # 从会话中获取用户信息
    get_flashed_messages()
    user_info = session.get('user')
    if user_info and user_info.get('loginstatus') == 1:
        return render_template('/user/userlogin.html', username=user_info.get('username'))
        # return render_template('userlogin.html',  username=user_info.get('username'), user_info=user_info)
        # return redirect(url_for('bookinfo', loginstatus=user_info.get('loginstatus', 1)))
    else:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))

# 退出登录
@app.route('/logout')
def logout():
    session.pop('user', None)  # 清空 Session 中的用户信息
    return redirect(url_for('index'))  # 重定向到登录页面或其他页面

# 图书信息
# @app.route('/bookinfo', methods=['GET'])
# def bookinfo():
#     result = query_data(sql="SELECT * FROM bookinfo")
#     if result:
#         return render_template('info.html', result=result)
#     else:
#         return "No user information found."
@app.route('/bookinfo')
def bookinfo():
    user_info = session.get('user')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    field_name_mapping = db_bookinfo()
    field_names, result = query_data(sql="SELECT * FROM bookinfo")
    if result:
        return render_template('/info.html', field_name_mapping=field_name_mapping, field_names=field_names, result=result, loginstatus=loginstatus)
    else:
        return "No user information found."
    
# 搜索
@app.route('/search', methods=['GET'])
def search():
    user_info = session.get('user')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    field_name_mapping = db_bookinfo()
    # 获取用户输入的关键词和固定数据
    keyword = request.args.get('keyword')
    fixed_data = request.args.get('fixed_data')

    if keyword:
        if fixed_data == "a":
            table_name = 'bookinfo'

        sql = 'SELECT * FROM {} WHERE bookid LIKE "%{}%" OR bookname LIKE "%{}%" \
            OR author LIKE "%{}%" OR remaining LIKE "%{}%"'.format(table_name, keyword, keyword, keyword, keyword)
        
        field_names, result = query_data(sql)

        if result:
            return render_template('/info.html',field_name_mapping=field_name_mapping, field_names=field_names, result=result, loginstatus=loginstatus)
        else:
            return "<script>alert('没用匹配的信息！'); window.location.href = '/';</script>"
    return "<script>alert('请输入查找的信息！'); window.location.href = '/';</script>"


# 用户搜索
@app.route('/user/usersearch', methods=['GET'])
def usersearch():
    # 数据库字段名对应网站映射
    field_name_mapping = db_bookinfo()
    user_info = session.get('user')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0

    # 获取用户输入的关键词和固定数据
    keyword = request.args.get('keyword')
    fixed_data = request.args.get('fixed_data')

    if keyword:
        if fixed_data == "a":
            table_name = 'bookinfo'

        sql = 'SELECT * FROM {} WHERE bookid LIKE "%{}%" OR bookname LIKE "%{}%" \
            OR author LIKE "%{}%" OR remaining LIKE "%{}%"'.format(table_name, keyword, keyword, keyword, keyword)
        
        field_names, result = query_data(sql)
        # append_to_file(field_names)

        if result:
            return render_template('/user/userbookinfo.html',field_name_mapping=field_name_mapping, field_names=field_names, result=result, loginstatus=loginstatus)
        else:
            return 'No matching data found.'
    return "<script>alert('请输入查找的信息！'); window.location.href = '/user/userlogin';</script>"

# 用户信息
@app.route('/user/userinfo', methods=['GET'])
def userinfo():
    user_info = session.get('user')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    if user_info and loginstatus==1:
        username = user_info['username']
        password = user_info['password']
        role = user_info['role']
        if role==1:
            flag='管理员'
        elif role==0:
            flag='普通用户'
        return render_template('/user/userinfo.html', username=username, password=password, role=flag)
    else:
        return redirect(url_for('login'))

# 用户借用教室搜索界面
@app.route('/user/borrowinfo', methods=['GET', 'POST'])
def borrowinfo():
    flag = None
    if '_flashes' in session:
        flag = session['_flashes'][0][1]
    
    user_info = session.get('user')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    if user_info and loginstatus == 1:
        # number = book_number(user_info['username'])
        # if number > 3:
        #     return '只能同时借用3本书'
        username = user_info['username']
        borrow_sql = 'SELECT borrow FROM usersborrow WHERE username="{}"'.format(username)
        _, data = query_data(borrow_sql)

        field_name_mapping = db_bookinfo()

        if request.method == 'POST':
            keyword = request.form['keyword']
            # append_to_file(str(keyword))
            if keyword:
                sql = 'SELECT * FROM bookinfo WHERE bookid LIKE "%{}%" OR bookname LIKE "%{}%" \
                OR author LIKE "%{}%" OR remaining LIKE "%{}%"'.format(keyword, keyword, keyword, keyword)
                field_names, result = query_data(sql)
            else:
                return 'a'
        elif request.method == 'GET':
            field_names, result = query_data(sql="SELECT * FROM bookinfo")

        name_sql = 'SELECT bookname FROM bookinfo WHERE bookid IN (SELECT borrow FROM usersborrow WHERE username="{}")'.format(username)
        _, bookid = query_data(name_sql)
        book_number = len(data)

        # append_to_file(str(result))

        return render_template('/user/usersborrow.html', messages=flag or "", field_name_mapping=field_name_mapping, \
                            field_names=field_names, result=result, loginstatus=loginstatus, \
                                book_number=book_number, username=username, bookid=bookid)
        # return str(number)
        
    else:
        return redirect(url_for('login'))
    # 备份
    # user_info = session.get('user')
    # loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    # if user_info and loginstatus == 1:
    #     # number = book_number(user_info['username'])
    #     # if number > 3:
    #     #     return '只能同时借用3本书'
    #     username = user_info['username']
    #     borrow_sql = 'SELECT borrow FROM usersborrow WHERE username="{}"'.format(username)
    #     _, data = query_data(borrow_sql)

    #     field_name_mapping = db_bookinfo()
    #     field_names, result = query_data(sql="SELECT * FROM bookinfo")

    #     name_sql = 'SELECT bookname FROM bookinfo WHERE bookid IN (SELECT borrow FROM usersborrow WHERE username="{}")'.format(username)
    #     _, bookid = query_data(name_sql)
    #     book_number = len(data)
    #     return render_template('usersborrow.html', field_name_mapping=field_name_mapping, \
    #                         field_names=field_names, result=result, loginstatus=loginstatus, \
    #                             book_number=book_number, username=username, bookid=bookid)
    #     # return str(number)
        
    # else:
    #     return redirect(url_for('login'))
        
# 借用功能
@app.route('/user/borrowbook', methods=['GET', 'POST'])
def borrowbook():
    get_flashed_messages()
    user_info = session.get('user')
    if request.method == 'POST':
        bookid = request.form['bookid']
        
        number_sql = 'SELECT borrow FROM usersborrow WHERE username="{}"'.format(user_info['username'])
        _, data = query_data(number_sql)
        book_number = len(data)     # 查询当前用户已经借用书本的数量

        remaining_sql = 'SELECT remaining FROM bookinfo WHERE bookid="{}"'.format(bookid)
        _, remaining_book = query_data(remaining_sql)   # 查询当前借用书本有无余量

        have_sql = 'SELECT id FROM usersborrow WHERE borrow="{}" AND username="{}"'.format(bookid, user_info['username'])
        _, have_data = query_data(have_sql)     #查询当前用户有无正在借用这本书

        if have_data:
            flash("已经借着这本书，禁止借用相同的书！")
            return redirect(url_for('borrowinfo'))
        elif book_number >= 3:
            # 弹窗不允许借用
            # 重定向到上一个页面
            flash("每个用户最多同时借用3本书, 当前用户已借用3本书, 禁止借用！")
            return redirect(url_for('borrowinfo'))
        
        elif remaining_book[0][0]==0:
            # 弹出当前书本余量为0，禁止借用
            flash("当前借阅书本余量为0, 借用失败！")
            return redirect(url_for('borrowinfo'))
        
        elif book_number < 3:
            # 更新书本余量的值
            sql1 = 'UPDATE bookinfo SET remaining = remaining - 1 WHERE bookid = %s AND remaining > 0;'
            update_data(sql1, bookid)

            # 更新用户借用的书本
            sql2 = 'INSERT INTO usersborrow (username, borrow) VALUES ({}, %s);'.format(user_info['username'])
            update_data(sql2,  bookid)
            flash("借用成功！")
            return redirect(url_for('borrowinfo'))


        # if 'bookid' in request.form and 'booklen' in request.form:
        #     bookid = request.form['bookid']
        #     # booklen = request.form['booklen']
        #     append_to_file(str(bookid)+'----')
        #     return bookid+'--'+user_info['username']  
        # else:
        #     return 'Missing bookid or booklen in the request.'

# 还书功能
@app.route('/user/breakbook', methods=['GET', 'POST'])
def breakbook():
    get_flashed_messages()
    user_info = session.get('user')
    if request.method == 'POST':
        bookname = request.form['bookname']
        sql = 'SELECT bookid FROM bookinfo WHERE bookname = "{}"'.format(bookname)
        _, bookid = query_data(sql)

        delete_sql = 'DELETE FROM usersborrow WHERE username = %s AND borrow = %s;'
        update_data(delete_sql, (user_info['username'], bookid))

        update_sql = 'UPDATE bookinfo SET remaining = remaining + 1 WHERE bookid = %s ;'
        update_data(update_sql, bookid)

        flash("归还成功！")
        return redirect(url_for('borrowinfo'))
    else:
        return redirect(url_for('userlogin'))


# 管理员模块
# 登录
@app.route('/admins', methods=['GET', 'POST'])
@app.route('/admins/logins', methods=['GET', 'POST'])
def logins():
    if request.method == 'GET':
        return render_template('admins/logins.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 调用登录验证函数
        if login_auth('admins', username, password):
            # 验证成功，将用户信息存储在会话中
            session['admins'] = {
                'username': username,
                'password': password,  # 示例邮箱
                'role': 1,
                'loginstatus': 1,
            }
            return redirect(url_for('admins_logins'))
        else:
            # 验证失败，返回错误信息或重定向到登录页面
            return redirect(url_for('logins', login_error=True))
        
# 登录进去后的界面
@app.route('/admins/logins/adminslogins', methods=['GET', 'POST'])
def admins_logins():
    get_flashed_messages()
    user_info = session.get('admins')
    if user_info and user_info.get('loginstatus') == 1:
        return render_template('admins/adminslogins.html', username=user_info['username'])
        # return render_template('userlogin.html',  username=user_info.get('username'), user_info=user_info)
        # return redirect(url_for('bookinfo', loginstatus=user_info.get('loginstatus', 1)))
    else:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('logins'))

# 退出登录
@app.route('/admins/logins/logouts')
def logouts():
    session.pop('admins', None)  # 清空 Session 中的用户信息
    return redirect(url_for('index'))  # 重定向到登录页面或其他页面

# 管理员搜索
@app.route('/admins/logins/adminssearch', methods=['GET', 'POST'])
def adminssearch():
    if request.method == 'POST':
        keyword = request.form['keyword']
        search_option = request.form.get('search_option')
    
    else:
        data_info = session.get('data')
        keyword = data_info['keyword']
        search_option = data_info['search_option']
        session.pop('data', None)   # 清空 Session 中的data信息

    user_info = session.get('admins')
    if search_option == 'bookinfo':
        field_name_mapping = db_bookinfo()
        sql = 'SELECT * FROM bookinfo WHERE bookid LIKE "%{}%" OR bookname LIKE "%{}%" \
        OR author LIKE "%{}%" OR remaining LIKE "%{}%"'.format(keyword, keyword, keyword, keyword)

    elif search_option == 'users':
        field_name_mapping = db_users()
        sql = 'SELECT * FROM users WHERE username LIKE "%{}%" OR password LIKE "%{}%" '.format(keyword, keyword)

    session['data'] = {
        'keyword' : keyword,
        'search_option' : search_option,
    }

    field_names, result = query_data(sql)
    return render_template('/admins/adminslogins.html', username=user_info['username'], \
                            field_name_mapping=field_name_mapping, field_names=field_names, result=result)

# 管理员信息
@app.route('/admins/logins/adminsinfo', methods=['GET', 'POST'])
def adminsinfo():
    user_info = session.get('admins')
    field_name_mapping = db_admins()
    sql = 'SELECT * FROM admins;'
    field_names, result = query_data(sql)
    return render_template('admins/adminsinfo.html',username=user_info['username'], field_names=field_names, field_name_mapping=field_name_mapping, result=result)

# 图书信息删除
@app.route('/admins/logins/adminsdelete', methods=['GET', 'POST'])
def adminsdelete():
    if request.method == 'POST':
        columns = request.form['columns']
        field_names = request.form['field_names']

        # data = session.get('data')
        # # keyword = data['keyword']
        # # search_option = data['search_option']

        # session.pop('data', None)   # 清空 Session 中的data信息

        users_key = str(list(db_users().keys()))
        bookinfo_key = str(list(db_bookinfo().keys()))

        if field_names == users_key:
           delete_sql = 'DELETE FROM users WHERE username = %s;'
        
        elif field_names == bookinfo_key:
            delete_sql = 'DELETE FROM bookinfo WHERE bookid = %s;'
        
        update_data(delete_sql, columns)
        
        # append_to_file(str(keyword))
        return redirect(url_for('adminssearch'))
        
# 查询修改的信息
@app.route('/admins/logins/adminschangeinfo', methods=['GET', 'POST'])
def adminschangeinfo():
    user_info = session.get('admins')
    loginstatus = 1 if user_info and user_info.get('loginstatus') == 1 else 0
    if request.method == 'POST':
        get_field_names = request.form['field_names']   # 表头（判断什么表）
        get_columns = request.form['columns']     # id表中第一个数据
        session.pop('datas', None)  # 清空 Session 中的datas信息
        session['datas'] = {
                'get_field_names' : get_field_names,
                'get_columns' : get_columns
            }
    else:
        # append_to_file('111')
        if session.get('datas'):
            data = session.get('datas')
            # session.pop('datas', None)  # 清空 Session 中的datas信息
            get_field_names = data['get_field_names']
            get_columns = data['get_columns']

    

    users_key = str(list(db_users().keys()))
    bookinfo_key = str(list(db_bookinfo().keys()))

    # 判断是什么表
    if get_field_names == users_key:
        field_name_mapping = db_users()
        select_sql = 'SELECT * FROM users WHERE id = {}'.format(get_columns)
    elif get_field_names == bookinfo_key:
        field_name_mapping = db_bookinfo()
        select_sql = 'SELECT * FROM bookinfo WHERE id = {}'.format(get_columns)

    field_names, result = query_data(select_sql)

    # 反转xy数据
    formatted_data = [(field_names[i], result[0][i]) for i in range(len(field_names))]

    return render_template('admins/adminschangeinfo.html', username=user_info['username'],\
                    formatted_data=formatted_data, field_name_mapping=field_name_mapping, loginstatus=loginstatus)
    
        # return render_template('admins/adminschangeinfo.html', username=user_info['username'],\
        #                         result=result, field_names=field_names, field_name_mapping=field_name_mapping, loginstatus=loginstatus)
    #return render_template('admins/adminschangeinfo.html', username=user_info['username'])

# 管理员修改信息
@app.route('/admins/logins/adminschange', methods=['GET', 'POST'])
def adminschange():
    
    form_data = request.form
    
    # 不允许修改已经存在的bookid
    id = form_data['id']
    if 'bookid' in form_data:
        bookid = form_data['bookid']
        _, result = query_data(sql='SELECT * FROM bookinfo WHERE bookid="{}" AND id != "{}"'.format(bookid, id))
        if result:
            return "<script>alert('不能使用相同的书号，请重新修改！'); window.location.href = '/admins/logins/adminschangeinfo';</script>"
        
        bookname = form_data['bookname']
        author = form_data['author']
        remaining = form_data['remaining']

        update_sql = 'UPDATE bookinfo SET bookid = %s, bookname = %s, author = %s, remaining = %s WHERE id = %s'
        data_update = (bookid, bookname, author, remaining, id)
        update_data(update_sql, data_update)
        return "<script>alert('书的信息修改成功！'); window.location.href = '/admins/logins/adminssearch';</script>"
    else:
        username = form_data['username']
        _, result = query_data(sql='SELECT * FROM users WHERE username="{}" AND id != "{}"'.format(username, id))
        if result:
            return "<script>alert('不能使用相同的账户，请重新修改！'); window.location.href = '/admins/logins/adminschangeinfo';</script>"
        
        password = form_data['password']

        update_sql = 'UPDATE users SET username = %s, password = %s WHERE id = %s'
        data_update = (username, password, id)
        update_data(update_sql, data_update)
        return "<script>alert('账户信息修改成功！'); window.location.href = '/admins/logins/adminssearch';</script>"
    # 返回适当的响应，比如重定向或者渲染一个成功页面

# 新增信息界面
@app.route('/admins/logins/adminsadd', methods=['GET', 'POST'])
def adminsadd():
    if request.method == 'POST':
        user_info = session.get('admins')
        info = request.form['info']     # str
        if info == list(db_bookinfo())[1]:
            # bookinfo
            field_name_mapping = db_bookinfo()
            del field_name_mapping['id']
            return render_template('admins/adminsadd.html', field_name_mapping=field_name_mapping, username=user_info['username'])
        
        else:
            # users
            field_name_mapping = db_users()
            del field_name_mapping['id']
            return render_template('admins/adminsadd.html', field_name_mapping=field_name_mapping, username=user_info['username'])

# 新增信息
@app.route('/admins/logins/adminsadds', methods=['GET', 'POST'])
def adminsadds():
    if request.method == 'POST':
        info = request.form['info']
        if info == '账号':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            if str(role) == '1':
                _, result = query_data(sql='SELECT * FROM admins WHERE username="{}"'.format(username))
                if result:
                    return "<script>alert('不能新增相同的管理员账户，请重新修改！'); window.location.href = '/admins/logins/adminssearch';</script>"
                
                update_sql = 'INSERT INTO admins (username, password, role) VALUES (%s, %s, 1);'
                update_data(update_sql, (username, password))
                return "<script>alert('管理员新增成功！'); window.location.href = '/admins/logins/adminssearch';</script>"
            
            else:
                _, result = query_data(sql='SELECT * FROM users WHERE username="{}"'.format(username))
                if result:
                    return "<script>alert('不能新增相同的用户账户，请重新修改！'); window.location.href = '/admins/logins/adminssearch';</script>"
                
                register_user(username, password)
                return "<script>alert('用户新增成功！'); window.location.href = '/admins/logins/adminssearch';</script>"
            
        elif info == '书号':
            bookid = request.form['bookid']
            _, result = query_data(sql='SELECT * FROM bookinfo WHERE bookid="{}"'.format(bookid))
            if result:
                return "<script>alert('不能新增相同的书号，请重新修改！'); window.location.href = '/admins/logins/adminssearch';</script>"
            
            bookname = request.form['bookname']
            author = request.form['author']
            remaining = request.form['remaining']
            update_sql = 'INSERT INTO bookinfo (bookid, bookname, author, remaining) VALUES (%s, %s, %s, %s);'
            update_data(update_sql, (bookid, bookname, author, remaining))
            return "<script>alert('图书信息新增成功！'); window.location.href = '/admins/logins/adminssearch';</script>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)
