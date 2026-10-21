
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
    "open": 7,
    "close": 22
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai"
]


MENU = [
    {"id": 1, "name": "Cà phê đen", "price": 20000},
    {"id": 2, "name": "Cà phê sữa", "price": 25000},
    {"id": 3, "name": "Bạc xỉu", "price": 30000},
    {"id": 4, "name": "Trà đào", "price": 25000},
    {"id": 5, "name": "Trà sữa", "price": 30000},
    {"id": 6, "name": "Nước cam", "price": 28000},
    {"id": 7, "name": "Sinh tố bơ", "price": 35000}
]



@app.get("/")
def index():
    hour = request.args.get("gio", type=int)

    if hour is None:
        hour = datetime.now().hour

    is_open = SHOP["open"] <= hour < SHOP["close"]

    return render_template(
        "index.html",
        shop=SHOP,
        hour=hour,
        is_open=is_open,
        promotions=PROMOTIONS
    )



@app.get("/menu")
def menu_page():
    page = request.args.get("page", default=1, type=int)

    per_page = 3
    total_pages = (len(MENU) + per_page - 1) // per_page

    if page < 1 or page > total_pages:
        return render_template("404.html", shop=SHOP), 404

    start = (page - 1) * per_page
    end = start + per_page

    menu_page_items = MENU[start:end]

    return render_template(
        "menu.html",
        shop=SHOP,
        menu=menu_page_items,
        page=page,
        pages=total_pages
    )



@app.get("/contact")
def contact():
    return render_template(
        "contact.html",
        shop=SHOP
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", shop=SHOP), 404


if __name__ == "__main__":
    app.run(debug=True)
