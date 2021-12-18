from flask import Flask, render_template, session
from datetime import timedelta
from auth import auth, login_required

app = Flask(__name__)
app.secret_key = "JKHJHjkhJKGhjgFgjfhj&45645645648678744654564s64dsdsdhghkghjfd"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.register_blueprint(auth)


@app.route('/')
def landing_page():
    return render_template('login.html')


@app.route('/register')
def register_user():
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard_user():
    username = session.get("user")
    return render_template('dashboard.html', username=username)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def page_erro(e):
    # note that we set the 500 status explicitly
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
