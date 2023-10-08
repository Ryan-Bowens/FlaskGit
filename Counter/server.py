from flask import Flask, render_template, redirect, session
app = Flask(__name__)
app.secret_key = 'Keep it secret, keep it safe'

@app.route('/')
def counter_base():
    if 'count' in session:
        session['count'] +=1
    else:
        session['count'] =1
    return render_template('index.html', count=session['count'])

@app.route('/plustwo')
def add_two():
    session['count'] += 2
    return render_template('index.html', count=session['count'])

@app.route('/destroy_session')
def reset():
    session.clear()
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)