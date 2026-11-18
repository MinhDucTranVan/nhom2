from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Integer, ForeignKey

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_key_nha_sach"
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
    title: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    nhaxuatban: Mapped[str] = mapped_column(String(200), default="")
    namxuatban: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)  # Tồn kho
    description: Mapped[str] = mapped_column(Text, default="")
    anhbia: Mapped[str] = mapped_column(String(255), default="")

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="books")


with app.app_context():
    db.create_all()


@app.context_processor
def inject_cart_count():
    gio_hang = session.get("gio_hang", {})
    tong_so_luong = sum(gio_hang.values())
    return dict(tong_so_luong_gio_hang=tong_so_luong)


@app.get("/books")
@app.get("/")
def danh_sach_sach():
    tu_khoa = request.args.get("tu_khoa", "").strip()
    ma_danh_muc = request.args.get("ma_danh_muc", type=int)

    cau_lenh = db.select(Book)

    if tu_khoa:
        cau_lenh = cau_lenh.where(
            (Book.title.ilike(f"%{tu_khoa}%")) | (Book.author.ilike(f"%{tu_khoa}%"))
        )

    if ma_danh_muc:
        cau_lenh = cau_lenh.where(Book.category_id == ma_danh_muc)

    danh_sach = db.session.scalars(cau_lenh.order_by(Book.id.desc())).all()
    tat_ca_danh_muc = db.session.scalars(
        db.select(Category).order_by(Category.name)
    ).all()

    return render_template(
        "books.html",
        danh_sach_sach=danh_sach,
        tat_ca_danh_muc=tat_ca_danh_muc,
        tu_khoa=tu_khoa,
        ma_danh_muc_chon=ma_danh_muc,
    )


@app.get("/books/<int:ma_sach>")
def chi_tiet_sach(ma_sach):
    sach = db.session.get(Book, ma_sach)
    if not sach:
        return render_template("404.html"), 404

    gio_hang = session.get("gio_hang", {})
    so_luong_da_co = gio_hang.get(str(ma_sach), 0)
    so_luong_con_lai_co_the_mua = max(0, sach.quantity - so_luong_da_co)

    return render_template(
        "book_detail.html",
        sach=sach,
        so_luong_da_co=so_luong_da_co,
        so_luong_con_lai_co_the_mua=so_luong_con_lai_co_the_mua,
    )


@app.post("/gio-hang/them/<int:ma_sach>")
def them_vao_gio(ma_sach):
    sach = db.session.get(Book, ma_sach)
    if not sach:
        flash("Sách không tồn tại!", "danger")
        return redirect(request.referrer or url_for("danh_sach_sach"))

    try:
        so_luong_mua = int(request.form.get("so_luong", 1))
    except ValueError:
        so_luong_mua = 1

    if so_luong_mua <= 0:
        flash("Số lượng mua không hợp lệ!", "danger")
        return redirect(request.referrer or url_for("danh_sach_sach"))

    gio_hang = session.get("gio_hang", {})
    ma_sach_chuoi = str(ma_sach)
    so_luong_hien_co = gio_hang.get(ma_sach_chuoi, 0)

    if so_luong_hien_co + so_luong_mua > sach.quantity:
        con_lai = sach.quantity - so_luong_hien_co
        flash(
            f"Không đủ hàng! Trong giỏ đã có {so_luong_hien_co}, chỉ có thể mua thêm tối đa {con_lai} cuốn.",
            "danger",
        )
        return redirect(request.referrer or url_for("danh_sach_sach"))

    gio_hang[ma_sach_chuoi] = so_luong_hien_co + so_luong_mua
    session["gio_hang"] = gio_hang
    session.modified = True

    flash(f"Đã thêm {so_luong_mua} × {sach.title} vào giỏ hàng.", "success")
    return redirect(request.referrer or url_for("xem_gio_hang"))


@app.get("/cart")
@app.get("/gio-hang")
def xem_gio_hang():
    gio_hang = session.get("gio_hang", {})
    danh_sach_mon_hang = []
    tong_tien = 0

    if gio_hang:
        ds_ma_sach = [int(ma) for ma in gio_hang.keys()]
        sach_trong_db = db.session.scalars(
            db.select(Book).where(Book.id.in_(ds_ma_sach))
        ).all()
        tra_cuu_sach = {s.id: s for s in sach_trong_db}

        for ma_chuoi, so_luong in gio_hang.items():
            sach = tra_cuu_sach.get(int(ma_chuoi))
            if sach:
                thanh_tien = sach.price * so_luong
                tong_tien += thanh_tien
                danh_sach_mon_hang.append(
                    {"sach": sach, "so_luong": so_luong, "thanh_tien": thanh_tien}
                )

    return render_template(
        "cart.html", danh_sach_mon_hang=danh_sach_mon_hang, tong_tien=tong_tien
    )


@app.post("/gio-hang/cap-nhat/<int:ma_sach>")
def cap_nhat_gio_hang(ma_sach):
    hanh_dong = request.form.get("hanh_dong")
    gio_hang = session.get("gio_hang", {})
    ma_sach_chuoi = str(ma_sach)
    sach = db.session.get(Book, ma_sach)

    if ma_sach_chuoi in gio_hang:
        if hanh_dong == "tang":
            if sach and gio_hang[ma_sach_chuoi] < sach.quantity:
                gio_hang[ma_sach_chuoi] += 1
            else:
                flash("Đã đạt số lượng tồn kho tối đa!", "warning")
        elif hanh_dong == "giam":
            gio_hang[ma_sach_chuoi] -= 1
            if gio_hang[ma_sach_chuoi] <= 0:
                gio_hang.pop(ma_sach_chuoi, None)
        elif hanh_dong == "xoa":
            gio_hang.pop(ma_sach_chuoi, None)

        session["gio_hang"] = gio_hang
        session.modified = True

    return redirect(url_for("xem_gio_hang"))


@app.post("/gio-hang/xoa-tat-ca")
def xoa_toan_bo_gio_hang():
    session.pop("gio_hang", None)
    flash("Đã làm trống giỏ hàng.", "info")
    return redirect(url_for("xem_gio_hang"))


if __name__ == "__main__":
    app.run(debug=True)
