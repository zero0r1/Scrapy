from flask import Flask,render_template,request,Markup

app = Flask(__name__)

#@app.route('/')
#def index():
#    return 'Index Page'

#@app.route('/hello')
#def hello():
#    return 'Hello, World'

#@app.route('/')
#def index(): pass

#@app.route('/login')
#def login(): pass

#@app.route('/user/<username>')
#def profile(username): pass

#with app.test_request_context():
#    print url_for('index')
#    print url_for('login')
#    print url_for('login', next='/')
#    print url_for('profile', username='John Doe')

#http method
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        do_the_login()
#    else:
#        show_the_login_form()

#@app.route('/hello/')
#@app.route('/hello/<name>')
#def hello(name=None):
#    #template must be create a templates folder
#    return render_template('hello.html', name=name)
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != '' and request.form['password'] != '':
            return request.form['username']
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()