from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wakeonlan import send_magic_packet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    mac = db.Column(db.String(30))


@app.route("/")
def index():
    item_list = item.query.all()
    return render_template("base.html", item_list=item_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    mac = request.form.get("mac")
    new_item = item(title=title, mac=mac)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/wake/<int:item_id>")
def wake(item_id):
    wol = item.query.filter_by(id=item_id).first()

    send_magic_packet(wol.mac)

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:item_id>")
def delete(item_id):
    wol = item.query.filter_by(id=item_id).first()
    db.session.delete(wol)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
