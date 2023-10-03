from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Use /play'

# def play():
#     return render_template('index.html', times=3)

# def playX(x):
#     return render_template('index.html', times=x)

@app.route('/play')
@app.route('/play/<int:x>')
@app.route('/play/<color>')
@app.route('/play/<color>/<int:x>')
@app.route('/play/<int:x>/<color>')
def playXcolor(x=3, color='blue'):
    return render_template('index.html', times=x, color=color)


if __name__=="__main__": 
    app.run(debug=True) 