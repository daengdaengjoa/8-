from flask import Flask, render_template
app = Flask(__name__)

## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mypage')
def mypage():
	return 'This is My page!'

if __name__ == "__main__":
    app.run(debug=True)