from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Use /play'

@app.route('/play')
def play():
    return render_template('index.html', times=3)

@app.route('/play/<int:x>')
def playX(x):
    return render_template('index.html', times=x)

@app.route('/play/<int:x>/<color>')
def playXcolor(x, color):
    return render_template('index.html', times=x, color=color)


if __name__=="__main__": 
    app.run(debug=True) 