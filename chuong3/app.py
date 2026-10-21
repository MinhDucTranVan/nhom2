from flask import Flask, request as req

app = Flask(__name__)



@app.route('/')
@app.route("/index")
@app.route("/home")

def index():
    return f"<a href='/Trang-chu'>Trang chủ</a> <a href='{url_for(gioi_thieu)}'>Gioi thieu</a>"  

def home():
    return "Welcome to the Flask API!"

@app.route('/Gioi-thieu')
@app.route('/about')
def gioi_thieu():
    return "day la trang gioi thieu."

@app.route("/user/<username>")
def user_profile(username):
    return f"Hello, {username}!"

@app.route("/square/<float:x>")
def square(x):
    return f"The square of {x} is {x**2}."

@app.route("/square2/<x>")
def square2(x):
    return f"The square of {x} is {float(x)**2}."
@app.route("/sum/<strs>")
def tong(strs):
    # 1,2,3=6
    number = strs.split(',')
    total = sum(float(num) for num in number)
    return f"Tong cua {strs} là {total}."
@app.route("/tinh-toan")
def tinh_toan():
    a = req.args.get('a', type=float)
    b = req.args.get('b', type=float)
    op =req.args.get("op")
    if a is None or b is None or op is None:
        return "Vui lòng cung cấp đầy đủ các tham số a, b và op."
    if op == "add":
        return f"{a} + {b} = {a + b}"
    else:
        return "Phép toán không hợp lệ."
    

if __name__ == '__main__':
    app.run(debug=True)