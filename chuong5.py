
from flask import Flask, render_template, request
import math

app = Flask(__name__)


# Hàm kiểm tra dữ liệu chung
def kiemtra(giatri, min_value=None, max_value=None):
    try:
        so = float(giatri.strip().replace(",", "."))

        if not math.isfinite(so):
            return None, "Vui lòng nhập 1 số"

        if min_value is not None and so < min_value:
            return None, f"Giá trị phải từ {min_value} đến {max_value}"

        if max_value is not None and so > max_value:
            return None, f"Giá trị phải từ {min_value} đến {max_value}"

        return so, ""

    except (ValueError, TypeError):
        return None, "Vui lòng nhập 1 số"


# TRANG CHỦ CHƯƠNG 5
@app.route("/")
def trangchu():
    return render_template("chuong5/index.html")


# BÀI 1: MÁY TÍNH CƠ BẢN
@app.route("/maytinh", methods=["GET", "POST"])
def maytinh():
    a = ""
    b = ""
    op = "+"
    ketqua = ""
    loi_a = ""
    loi_b = ""

    if request.method == "POST":
        a = request.form.get("a", "").strip()
        b = request.form.get("b", "").strip()
        op = request.form.get("op", "+")

        so_a, loi_a = kiemtra(a)
        so_b, loi_b = kiemtra(b)

        if not loi_a and not loi_b:
            if op == "+":
                kq = so_a + so_b
            elif op == "-":
                kq = so_a - so_b
            elif op == "*":
                kq = so_a * so_b
            elif op == "/":
                if so_b == 0:
                    loi_b = "Không thể chia cho 0"
                else:
                    kq = so_a / so_b
            else:
                loi_b = "Phép toán không hợp lệ"

            if not loi_b:
                ketqua = f"{so_a:g} {op} {so_b:g} = {kq:g}"

    return render_template(
        "chuong5/maytinh.html",
        a=a,
        b=b,
        op=op,
        ketqua=ketqua,
        loi_a=loi_a,
        loi_b=loi_b
    )


# BÀI 2: TÍNH ĐIỂM HỌC PHẦN
@app.route("/tinhdiem", methods=["GET", "POST"])
def tinhdiem():
    cc = ""
    gk = ""
    ck = ""

    loi_cc = ""
    loi_gk = ""
    loi_ck = ""

    diem_hp = None
    diem_chu = ""
    ghi_chu = ""

    if request.method == "POST":
        cc = request.form.get("cc", "").strip()
        gk = request.form.get("gk", "").strip()
        ck = request.form.get("ck", "").strip()

        so_cc, loi_cc = kiemtra(cc, 0, 10)
        so_gk, loi_gk = kiemtra(gk, 0, 10)
        so_ck, loi_ck = kiemtra(ck, 0, 10)

        # Đổi thông báo lỗi theo yêu cầu
        for ten, loi in [
            ("cc", loi_cc),
            ("gk", loi_gk),
            ("ck", loi_ck)
        ]:
            if loi.startswith("Giá trị phải"):
                if ten == "cc":
                    loi_cc = "Điểm phải từ 0 đến 10"
                elif ten == "gk":
                    loi_gk = "Điểm phải từ 0 đến 10"
                else:
                    loi_ck = "Điểm phải từ 0 đến 10"

        if not loi_cc and not loi_gk and not loi_ck:
            diem_hp = round(
                so_cc * 0.1 +
                so_gk * 0.3 +
                so_ck * 0.6, 1
            )

            if so_ck < 1:
                diem_chu = "F"
                ghi_chu = "Điểm thi dưới 1"
            elif diem_hp >= 8.5:
                diem_chu = "A"
            elif diem_hp >= 7.5:
                diem_chu = "B"
            elif diem_hp >= 5.5:
                diem_chu = "C"
            elif diem_hp >= 4.0:
                diem_chu = "D"
            else:
                diem_chu = "F"

    return render_template(
        "chuong5/tinhdiem.html",
        cc=cc,
        gk=gk,
        ck=ck,
        loi_cc=loi_cc,
        loi_gk=loi_gk,
        loi_ck=loi_ck,
        diem_hp=diem_hp,
        diem_chu=diem_chu,
        ghi_chu=ghi_chu
    )


# BÀI 3: TÍNH CHỈ SỐ BMI
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    chieucao = ""
    cannang = ""

    loi_cc = ""
    loi_cn = ""

    bmi_value = None
    phanloai = ""
    mausac = ""
    cannang_min = None
    cannang_max = None

    if request.method == "POST":
        chieucao = request.form.get("chieucao", "").strip()
        cannang = request.form.get("cannang", "").strip()

        cc, loi_cc = kiemtra(chieucao, 50, 250)
        cn, loi_cn = kiemtra(cannang, 10, 300)

        if not loi_cc and not loi_cn:
            m = cc / 100
            bmi_value = round(cn / (m ** 2), 1)

            if bmi_value < 18.5:
                phanloai = "Thiếu cân"
                mausac = "warning"
            elif bmi_value < 23:
                phanloai = "Bình thường"
                mausac = "success"
            elif bmi_value < 25:
                phanloai = "Thừa cân"
                mausac = "warning"
            else:
                phanloai = "Béo phì"
                mausac = "danger"

            cannang_min = round(18.5 * m ** 2, 1)
            cannang_max = round(22.9 * m ** 2, 1)

    return render_template(
        "chuong5/bmi.html",
        chieucao=chieucao,
        cannang=cannang,
        loi_cc=loi_cc,
        loi_cn=loi_cn,
        bmi=bmi_value,
        phanloai=phanloai,
        mausac=mausac,
        cannang_min=cannang_min,
        cannang_max=cannang_max
    )


if __name__ == "__main__":
    app.run(debug=True)
