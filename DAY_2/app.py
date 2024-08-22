from flask import Flask ,request ,render_template,jsonify,flash,redirect,url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
from flask_migrate import Migrate



app = Flask(__name__)
app.secret_key = "secreate_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
CORS(app)
app.config['LOGIN_URL'] = '/login'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    user_name = db.Column(db.String(120), nullable=False)




@app.route('/login', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))  # Redirect authenticated users to the home page
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        check_user = User.query.filter_by(email=email).first()
        userBytes = password.encode('utf-8') 
        
        if check_user:
            hash = check_user.password  # Retrieve the hashed password from the database
            if bcrypt.checkpw(userBytes, hash):
                login_user(check_user)
                flash("Logged In")
                return redirect(url_for("home"))
            else:
                flash("Invalid Password")
                return render_template('login.html')
        else:
            flash("Invalid Email")
            return render_template('login.html')

    return render_template('login.html')




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_name = request.form["user_name"]
        try:
            # Hash the password
            bytes_password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(bytes_password, salt)
            
            # Store the hashed password as bytes
            create_user = User(email=email, password=hash_password, user_name=user_name)
            db.session.add(create_user)
            db.session.commit()
            flash("User created successfully!")
            return render_template("login.html")
        except Exception as e:
            flash(f"{e}")
            return render_template("register.html")
    return render_template("register.html")

        
@login_required       
@app.route("/home", methods=["GET"])
def home():
    print("inside home")
    user_name = current_user.user_name
    email = current_user.email
    id = current_user.id
    return render_template("home.html", user_name=user_name, email=email, id=id)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


#requirements.txt

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
