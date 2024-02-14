from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, make_response

from models import db, Shed, ShedData

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db.init_app(app)


@app.cli.command("create")
def create():
    with app.app_context():
        db.create_all()


def get_today_date():
    return str(datetime.now().date())


@app.context_processor
def inject_today():
    return {"today": get_today_date()}


@app.route("/")
def index():
    date = request.args.get("date", get_today_date())

    sheds = db.session.query(Shed).join(ShedData).filter(ShedData.date == date).all()
    response = make_response(render_template("index.html", sheds=sheds))

    # If this HTMX request then redirect instead of append.
    if "Hx-Request" in request.headers:
        response.headers.set("HX-Redirect", url_for("index", date=date))

    return response


@app.route("/shed")
def shed_index():
    sheds = db.session.execute(db.select(Shed)).scalars()
    return render_template("shed_index.html", sheds=sheds)


@app.route("/shed_create", methods=["GET", "POST"])
def shed_create():
    if request.method == "POST":
        name = request.form["name"]
        shed = Shed()
        shed.name = name
        db.session.add(shed)
        db.session.commit()
        return redirect(url_for("shed_index"))
    return render_template("shed_create.html")


@app.route("/shed_data_create/<shed_name>", methods=["GET", "POST"])
def shed_data_create(shed_name):
    if request.method == "POST":
        value = request.form["value"]

        shed = db.one_or_404(db.select(Shed).filter_by(name=shed_name))
        shed_data = ShedData()
        shed_data.shed = shed
        shed_data.date = str(datetime.now().date())
        shed_data.value = value
        db.session.add(shed_data)
        db.session.commit()
        return render_template("shed_data.html", shed_data=shed_data, shed=shed)
    return render_template("shed_data.html")


@app.route("/prepare", methods=["GET"])
def prepare():
    date = request.args.get("date", get_today_date())
    sheds = db.session.query(Shed).join(ShedData).filter(ShedData.date == date).all()

    total_milk = 0
    for shed in sheds:
        for child in shed.children:
            total_milk += child.value

    response = make_response(
        render_template("prepare.html", sheds=sheds, total_milk=total_milk)
    )

    # If this HTMX request then redirect instead of append.
    if "Hx-Request" in request.headers:
        response.headers.set("HX-Redirect", url_for("index", date=date))

    return response
