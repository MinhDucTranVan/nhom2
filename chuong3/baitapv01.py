from flask import Flask, request as req, url_for, render_template, jsonify
app = Flask(__name__)

BOOKS = [
    {
        "id": 1,
        "title": "Python cơ bản",
        "author": "Nguyễn Văn A",
        "year": 2024,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "Flask cơ bản",
        "author": "Nguyễn Văn B",
        "year": 2023,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 3,
        "title": "Lập trình Web",
        "author": "Trần Văn C",
        "year": 2022,
        "category": "Web",
        "available": False
    },
    {
        "id": 4,
        "title": "Cơ sở dữ liệu",
        "author": "Lê Văn D",
        "year": 2021,
        "category": "Cơ sở dữ liệu",
        "available": True
    }
]

@app.route('/')
def home ():
    tong_so_sach = len(BOOKS)
    so_sach_san_sang = sum(1 for book in BOOKS if book["available"])
    return f"Tong so sach: {tong_so_sach}, So sach san sang: {so_sach_san_sang}"

@app.route("/books")
def books():
    category = req.args.get("category")

    if category:
        books = [book for book in BOOKS if book["category"] == category]
    else:
        books = BOOKS

    return render_template("books.html", books=books)

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return render_template("book_detail.html", book=book)

    return f"Không có sách với ID = {book_id}", 404

@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)

@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return jsonify(book)

    return jsonify({
        "error": f"Không có sách với ID = {book_id}"
    }), 404
    



if __name__ == '__main__':
    app.run(debug=True)