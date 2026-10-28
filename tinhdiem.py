
from flask import Flask, render_template, request

app = Flask(__name__)


# Hàm kiểm tra chung cho cả 3 ô
def kiemtra(diem):
    try:
        so = float(diem.replace(",", "."))

        if not 0 <= so <= 10:
            return None, "Điểm phải từ 0 đến 10"

        return so, ""

    except ValueError:
        return None, "Vui lòng nhập 1 số"


@app.route("/", methods=["GET", "POST"])
def trangchu():
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

        # Dùng chung một hàm kiểm tra
        so_cc, loi_cc = kiemtra(cc)
        so_gk, loi_gk = kiemtra(gk)
        so_ck, loi_ck = kiemtra(ck)

        # Chỉ tính khi cả 3 điểm hợp lệ
        if not loi_cc and not loi_gk and not loi_ck:

            diem_hp = round(
                so_cc * 0.1 +
                so_gk * 0.3 +
                so_ck * 0.6, 1
            )

            # Kiểm tra điểm liệt trước
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
        "tinhdiem/trangchu.html",
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


if __name__ == "__main__":
    app.run(debug=True)
