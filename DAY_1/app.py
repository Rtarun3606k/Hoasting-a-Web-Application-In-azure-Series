from flask import Flask ,render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

lists = ["apple","banana","cherry"]


class Fruits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    # lists = ["apple","banana","cherry"]

    # return jsonify({"message":"Hello World","List_of_fruits" : lists  })
    lists = Fruits.query.all()
    return render_template("index.html", fruits = lists,name="Sahil")

@app.route("/add/data",methods=["POST"])
def add_data():
    data = request.form['fruit']
    # print(data)
    lists.append(data)
    add_data = Fruits(name=data)
    try:
        db.session.add(add_data)
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        return redirect(url_for("home"))
    # return redirect(url_for("home"))


if __name__ == '__main__':
    with app.app_context() :
        db.create_all() 
    app.run(debug=True)