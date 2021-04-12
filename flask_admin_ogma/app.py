from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager,UserMixin,login_required,current_user
import yfinance as yf

app = Flask(__name__)

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu18/workout1.db'
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)
admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

admin.add_view(ModelView(user, db.session))



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# @app.route("/")
# def index():
#     return render_template("index.html")



@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        print(uname,passw,'kkk')
        login = user.query.filter_by(email=uname, password=passw).first()
        if login is not None:
            print('lllllll')
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard",methods=["GET", "POST"])
# @login_required
def dashboard():
        
    if request.method == "POST":
        ncompany = request.form["ncompany"]
        print(ncompany,'kkkkkkk')
        if ncompany:
            print('lkljkkkkkkkkkkk')
            msft = yf.Ticker(ncompany)
            print(msft)
            print(msft.info)
            print(msft.history(period="max"))
    
            legend = ' Data'
            labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
            values = [10, 9, 8, 7, 6, 4, 7, 8]
        

    
            return render_template('dashboard.html', values=values, labels=labels, legend=legend)
    return render_template('dashboard.html')


@app.route('/get_data')
def get_prediction():
  word = flask.request.args.get('word')
  return flask.jsonify({'html':getPrediction(word)})

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         uname = request.form['uname']
#         mail = request.form['mail']
#         passw = request.form['passw']
#         print(uname,mail,passw,'lllllllllll')

#         register = user(username = uname, email = mail, password = passw)
#         db.session.add(register)
#         db.session.commit()

#         return redirect(url_for("login"))
#     return render_template("register.html")


@app.route('/table')
def table():
    User = user.query.all()
    return render_template('table.html',users = User)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port = 5002)