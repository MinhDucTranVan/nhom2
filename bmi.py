
from flask import Flask, render_template, request

app = Flask(__name__)


def kiemtra(giatri, min_value, max_value):
    try:
        so = float(giatri.replace(",", "."))

        if not min_value <= so <= max_value:
            return None, f"Giá trị phải từ {min_value} đến {max_value}"

        return so, ""

    except ValueError:
        return None, "Vui lòng nhập 1 số"


@app.route("/", methods=["GET", "POST"])
def trangchu():
    chieucao = ""
    cannang = ""

    loi_cc = ""
    loi_cn = ""

    bmi = None
    phanloai = ""
    mausac = ""
    cannang_min = None
    cannang_max = None

    if request.method == "POST":
        chieucao = request.form.get("chieucao", "").strip()
        cannang = request.form.get("cannang", "").strip()

        # Kiểm tra dữ liệu
        cc, loi_cc = kiemtra(chieucao, 50, 250)
        cn, loi_cn = kiemtra(cannang, 10, 300)

        if not loi_cc and not loi_cn:
            # Đổi cm sang m
            chieucao_m = cc / 100

            # Tính BMI
            bmi = round(cn / (chieucao_m ** 2), 1)

            # Phân loại
            if bmi < 18.5:
                phanloai = "Thiếu cân"
                mausac = "warning"

            elif bmi < 23:
                phanloai = "Bình thường"
                mausac = "success"

            elif bmi < 25:
                phanloai = "Thừa cân"
                mausac = "warning"

            else:
                phanloai = "Béo phì"
                mausac = "danger"

            # Khoảng cân nặng nên có
            cannang_min = round(18.5 * chieucao_m ** 2, 1)
            cannang_max = round(22.9 * chieucao_m ** 2, 1)

    return render_template(
        "bmi/trangchu.html",
        chieucao=chieucao,
        cannang=cannang,
        loi_cc=loi_cc,
        loi_cn=loi_cn,
        bmi=bmi,
        phanloai=phanloai,
        mausac=mausac,
        cannang_min=cannang_min,
        cannang_max=cannang_max
    )


if __name__ == "__main__":
    app.run(debug=True)
