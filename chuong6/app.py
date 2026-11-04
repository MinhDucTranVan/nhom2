
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, func


# ==============================
# 1. KHỞI TẠO FLASK VÀ DATABASE
# ==============================

class Base(DeclarativeBase):
    pass


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ==============================
# 2. KHAI BÁO MODEL STUDENT
# ==============================

class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    mssv: Mapped[str] = mapped_column(
        String(10),
        unique=True
    )

    name: Mapped[str] = mapped_column(String(100))

    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"<Student {self.mssv} {self.name}>"


# ==============================
# 3. TẠO DATABASE
# ==============================

with app.app_context():
    db.create_all()


# ==============================
# 4. KHAI BÁO TEXT RESPONSE
# ==============================

TEXT = {
    "Content-Type": "text/plain; charset=utf-8"
}


# ==============================
# 5. THÊM DỮ LIỆU MẪU
# ==============================

@app.get("/them-mau")
def them_mau():

    total = db.session.scalar(
        db.select(func.count(Student.id))
    )

    if total > 0:
        return f"Đã có {total} sinh viên, không thêm nữa.", TEXT

    students = [
        Student(
            mssv="23T1020001",
            name="Nguyễn Văn An",
            gpa=8.5
        ),
        Student(
            mssv="23T1020002",
            name="Trần Thị Bình",
            gpa=6.8
        ),
        Student(
            mssv="23T1020003",
            name="Lê Hoàng Cường",
            gpa=9.1
        ),
        Student(
            mssv="23T1020004",
            name="Phạm Minh Dũng",
            gpa=4.5
        ),
        Student(
            mssv="23T1020005",
            name="Hoàng Thu Hà",
            gpa=7.4
        )
    ]

    db.session.add_all(students)
    db.session.commit()

    return "Đã thêm 5 sinh viên thành công!", TEXT


# ==============================
# 6. ĐỌC DỮ LIỆU BẰNG VIEW FUNCTION
# ==============================

@app.get("/thu-truy-van")
def try_queries():

    # Kiểm tra database có dữ liệu không
    if db.session.scalar(
        db.select(func.count(Student.id))
    ) == 0:
        return "Chưa có dữ liệu, hãy mở /them-mau trước.", TEXT

    lines = []

    # 1. Lấy sinh viên có ID = 3
    lines.append(
        f"1. get(3): {db.session.get(Student, 3)}"
    )

    # 2. Lấy sinh viên có ID = 99
    lines.append(
        f"2. get(99): {db.session.get(Student, 99)}"
    )

    # 3. Lấy tất cả sinh viên
    everyone = db.session.scalars(
        db.select(Student)
    ).all()

    lines.append(
        f"3. Tất cả: {len(everyone)} sinh viên"
    )

    # 4. Lấy sinh viên có GPA >= 8
    stmt = (
        db.select(Student)
        .where(Student.gpa >= 8)
        .order_by(Student.gpa.desc())
    )

    good = db.session.execute(stmt).scalars().all()

    lines.append(
        f"4. Điểm >= 8: {good}"
    )

    # 5. Tìm sinh viên theo MSSV
    binh = db.session.scalar(
        db.select(Student).filter_by(
            mssv="23T1020002"
        )
    )

    lines.append(
        f"5. MSSV 23T1020002: {binh}"
    )

    # 6. Đếm số sinh viên
    count = db.session.scalar(
        db.select(func.count(Student.id))
    )

    # Tính điểm trung bình
    avg = db.session.scalar(
        db.select(func.avg(Student.gpa))
    )

    lines.append(
        f"6. Số SV: {count}, điểm TB: {avg:.2f}"
    )

    return "\n".join(lines), TEXT

@app.get("/danh-sach")
def danh_sach():
    students = db.session.scalars(
        db.select(Student).order_by(Student.id)
    ).all()

    return render_template(
        "danh_sach.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)
