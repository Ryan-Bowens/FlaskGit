from flask import Flask, render_template, session, request, redirect
app = Flask(__name__)
app.secret_key = 'Kepe it secret, keep it safe'

@app.route('/')
def landing():
    return render_template('index.html')


@app.route('/process', methods=['post'])
def process():
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['language'] = request.form['language']
    session['comments'] = request.form['comments']
    return redirect('/result')

@app.route('/result')
def result():
    return render_template('result.html', name=session['name'], location=session['location'], language=session['language'], comments=session['comments'])

if __name__=="__main__":
    app.run(debug=True)