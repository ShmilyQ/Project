from flask import Flask,request

app = Flask(__name__)

# 路由的定义
@app.route('/book/list')
# 处理函数
def book_list():
    # 获取请求参数
    # 如果没有传递page参数，则默认值为1
    page = request.args.get("page", default = 1, type = int)

    # 返回当前页数
    return f"当前是第{page}页书籍列表"

# 带参数的路由，<>中的部分是变量，其中int表示该参数是整数类型,book_id是变量名;当访问/book/detail/1时，book_id的值为1，为空时会报错
# 此时的get请求为：127.0.0.1:5000/book/detail/1
@app.route('/book/detail/<int:book_id>')
def book_detail(book_id):
    # 返回书籍的详细信息
    return f"书籍ID为{book_id}的详细信息"

if __name__ == "__main__":
    app.run(debug=True, host= "127.0.0.1", port= 5000)