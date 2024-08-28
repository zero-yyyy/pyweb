'''
 自定义函数
'''
from server_conf import *
# 表定义
# 书
def db_bookinfo():
    return  {
        'id': 'ID',
        'bookid': '书号',
        'bookname': '书名',
        'author': '作者',
        'remaining': '有无余书',
    }

# 用户
def db_users():
    return  {
        'id': 'ID',
        'username': '账号',
        'password': '密码',
        'role': '账户权限',
    }

# 管理员
def db_admins():
     return  {
        'id': 'ID',
        'username': '账号',
        'password': '密码',
        'role': '账户权限',
    }

def append_to_file(data, filename='error.txt'):
    with open(filename, 'a') as file:
        file.write('\n')
        file.write(str(data))
    #print(f"数据已追加到文件 '{filename}' 中。")

# 查询数据
# def query_data(sql):
#     connection = pymysql.connect(**db_config)
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             return result
#     except Exception as e:
#         print(f"Error during query: {str(e)}")
#         return None
#     finally:
#         connection.close()
def query_data(sql):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            field_names = [i[0] for i in cursor.description]  # 获取字段名
            result = cursor.fetchall()
            return field_names, result
    except Exception as e:
        print(f"Error during query: {str(e)}")
        return None, None
    finally:
        connection.close()

# 登录
def login_auth(tables, username, password):
    sql = f"SELECT * FROM {tables} WHERE username = '{username}' AND password = '{password}'"
    _, result = query_data(sql)
    if result:
        return True
    else:
        return False

# 查询数据库，检查用户名是否已存在
def is_username_taken(username):
    sql = f"SELECT * FROM users WHERE username = '{username}'"
    _, result = query_data(sql)
    return len(result) > 0

# 注册用户并写入数据库
def register_user(username, password):
    sql = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except Exception as e:
        print(f"Error during registration: {str(e)}")
    finally:
        connection.close()

# 改变数据
def update_data(sql, data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            connection.commit()
            print("Data updated successfully.")
            append_to_file(cursor.mogrify(sql, data))
    except Exception as e:
        append_to_file(str(e))
        print(f"Error during update: {str(e)}")
    finally:
        connection.close()


