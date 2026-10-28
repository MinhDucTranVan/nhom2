
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def trangchu():
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

        # Kiểm tra số thứ nhất
        try:
            so_a = float(a.replace(",", "."))
        except ValueError:
            loi_a = "Vui lòng nhập 1 số"

        # Kiểm tra số thứ hai
        try:
            so_b = float(b.replace(",", "."))
        except ValueError:
            loi_b = "Vui lòng nhập 1 số"

        # Chỉ tính khi cả hai số hợp lệ
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

            if not loi_b:
                # Định dạng số gọn: 10.0 -> 10
                a_hien = format(so_a, "g")
                b_hien = format(so_b, "g")
                kq_hien = format(kq, "g")

                ketqua = f"{a_hien} {op} {b_hien} = {kq_hien}"

    return render_template(
        "calculator/trangchu.html",
        a=a,
        b=b,
        op=op,
        ketqua=ketqua,
        loi_a=loi_a,
        loi_b=loi_b
    )


if __name__ == "__main__":
    app.run(debug=True)
