from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    a = request.form.get("a")
    b = request.form.get("b")
    if a is None or b is None:
        a = 0
        b = 0
    else:
        a = int(a)
        b = int(b)
    chia= a/b if b != 0 else 'undefined'
    ketqua = {
        'cong': a + b,
        'tru': a - b,
        'nhan': a * b,
        'chia': chia
    }
    
    #return "xin chao"
    return render_template('math.html', a=a, b=b, ketqua=ketqua)

@app.route('/math')
def math():
    return render_template('math.html')

if __name__ == '__main__':
    app.run(debug=True) 
