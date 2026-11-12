from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Integer, ForeignKey


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quanly_sach.db"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    description: Mapped[str] = mapped_column(Text, default="")

    books: Mapped[list["Book"]] = relationship(back_populates="category")


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    author: Mapped[str] = mapped_column(String(100), nullable=False)

    price: Mapped[float] = mapped_column(Float, default=0)

    quantity: Mapped[int] = mapped_column(Integer, default=0)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="books")


with app.app_context():
    db.create_all()


@app.get("/")
def home():
    return "da ket noi"


@app.route("/dashboard")
def dashboard():
    so_danh_muc = Category.query.count()
    so_sach = Book.query.count()

    return render_template("dashboard.html", so_danh_muc=so_danh_muc, so_sach=so_sach)


@app.route("/danh-muc")
def danh_muc():
    danh_muc = Category.query.all()

    return render_template("danh_muc.html", danh_muc=danh_muc)


@app.route("/them-danh-muc", methods=["POST"])
def them_danh_muc():
    ten = request.form.get("name")
    mo_ta = request.form.get("description")

    danh_muc = Category(name=ten, description=mo_ta)

    db.session.add(danh_muc)
    db.session.commit()

    return redirect(url_for("danh_muc"))


@app.route("/sua-danh-muc/<int:id>", methods=["GET", "POST"])
def sua_danh_muc(id):
    danh_muc = db.session.get(Category, id)

    if danh_muc is None:
        return "khong thay danh muc nao"

    if request.method == "POST":
        danh_muc.name = request.form.get("name")
        danh_muc.description = request.form.get("description")

        db.session.commit()

        return redirect(url_for("danh_muc"))

    return render_template("sua_danh_muc.html", danh_muc=danh_muc)


@app.route("/xoa-danh-muc/<int:id>", methods=["POST"])
def xoa_danh_muc(id):
    danh_muc = db.session.get(Category, id)

    if danh_muc is None:
        return "K thấy danh mục"

    if danh_muc.books:
        return "K xóa được!"

    db.session.delete(danh_muc)
    db.session.commit()

    return redirect(url_for("danh_muc"))


@app.route("/sach")
def sach():
    danh_muc = Category.query.all()
    ds_sach = Book.query.all()

    return render_template("sach.html", danh_muc=danh_muc, ds_sach=ds_sach)


@app.route("/them-sach", methods=["POST"])
def them_sach():
    ten_sach = request.form.get("title")
    tac_gia = request.form.get("author")
    gia = request.form.get("price")
    so_luong = request.form.get("quantity")
    ma_danh_muc = request.form.get("category_id")

    sach = Book(
        title=ten_sach,
        author=tac_gia,
        price=float(gia),
        quantity=int(so_luong),
        category_id=int(ma_danh_muc),
    )

    db.session.add(sach)
    db.session.commit()

    return redirect(url_for("sach"))


@app.route("/sua-sach/<int:id>", methods=["GET", "POST"])
def sua_sach(id):
    sach = db.session.get(Book, id)
    danh_muc = Category.query.all()

    if sach is None:
        return "Không tìm thấy sách!"

    if request.method == "POST":
        sach.title = request.form.get("title")
        sach.author = request.form.get("author")
        sach.price = float(request.form.get("price"))
        sach.quantity = int(request.form.get("quantity"))
        sach.category_id = int(request.form.get("category_id"))

        db.session.commit()

        return redirect(url_for("sach"))

    return render_template("sua_sach.html", sach=sach, danh_muc=danh_muc)


@app.route("/xoa-sach/<int:id>", methods=["POST"])
def xoa_sach(id):
    sach = db.session.get(Book, id)

    if sach is None:
        return "Không tìm thấy sách!"

    db.session.delete(sach)
    db.session.commit()

    return redirect(url_for("sach"))


if __name__ == "__main__":
    app.run(debug=True)
