from flask import Flask, render_template

app = Flask(__name__)
# 定义带参路由，用于接收书籍项目数
@app.route('/book/<int:count>')
# 定义视图函数，接收参数并渲染模板
def book(count):
    # 渲染模板，传递参数，其中index.html为渲染的网页 ，count 是书籍项目数，userName 是用户名
    return render_template('index.html', count=count, userName="John Doe")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)