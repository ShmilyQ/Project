from flask import Flask, render_template, request, redirect, url_for

# 使用Flask创建一个app应用
# __name__是一个特殊变量，表示当前模块的名称
# 1. 以后出现bug时，可以通过__name__来定位问题
# 2. Flask会根据__name__来查找静态文件和模板文件，有一个默认的路径
app = Flask(__name__)

# 创建一个路由和视图函数的映射关系
# 路由是URL和视图函数的对应关系
@app.route('/', methods=['post'])
def hello():
    # 返回一个字符串
    return 'Hello, Flask!!!!!!!'

# app.route()装饰器用于定义路由
# host和port参数用于指定Flask应用的运行地址和端口
# __main__是一个特殊变量，表示当前模块是否是主模块
# __name__ == '__main__'表示当前模块是主模块, 如果当前模块是主模块，则执行以下代码
if __name__ == '__main__':
    # 运行Flask应用
    # debug=True表示开启调试模式，自动重载代码
    app.run(debug=True, host='0.0.0.0', port=5000)
