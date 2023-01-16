from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.title} --- {self.desc}"


@app.route("/", methods=["GET", "POST"])
def home():
    todo_list = Todo.query.all()
    return render_template("post_data.html", todo_list=todo_list)


@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    todo = Todo.query.filter_by(sno=todo_id).first()
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("home"))

    else:
        return render_template("update.html", todo=todo)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(sno=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if len(title) == 0:
            abort(404, {"message": "Title cannot be empty"})
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5500, threaded=True)
