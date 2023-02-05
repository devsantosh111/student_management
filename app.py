from flask import Flask, render_template, request, jsonify
import sqlite3
from student import Student

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    try:
        db = sqlite3.connect("student.db").cursor()
        db.execute('''CREATE TABLE IF NOT EXISTS STUDENTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, department TEXT
            )''')
        db.close()
    except Exception as e:
        print(e)
    finally:
        return render_template('index.html')

@app.route("/add", methods=["POST", "GET"])
def add_student():
    try:
        sqlite = sqlite3.connect("student.db")
        db = sqlite.cursor()
        student = Student(request.json["firstname"],
                      request.json["lastname"],
                      request.json["department"]
                      )
        # print(student)
        db.execute('''INSERT INTO STUDENTS(firstname, lastname, department) VALUES(?,?,?)''',(student.f_name, student.l_name, student.department))
        sqlite.commit()
        return jsonify({"detail":"student data added successfully"})
    except Exception as e:
        return jsonify({"detail":"Something went wrong"})

@app.route("/students", methods=["GET"])
def view_students():
    try:
        db = sqlite3.connect("student.db").cursor()
        db.execute('''SELECT * FROM STUDENTS''')
        data = db.fetchall()
        result = []
        for d in data:
            obj = {}    
            obj["id"] = d[0]
            obj["firstname"] = d[1]
            obj["lastname"] = d[2]
            obj["department"] = d[3]
            result.append(obj)
        return jsonify(result)
    except Exception as e:
        return jsonify({"detail":"Something went wrong"})

@app.route("/student/<id>", methods=["GET"])
def get_student(id):
    try:
        db = sqlite3.connect("student.db").cursor()
        exists = db.execute('''SELECT * FROM STUDENTS WHERE id=?''', (id,)).fetchone()
        if exists is not None:
            obj = {}
            obj["id"] = exists[0]
            obj["firstname"] = exists[1]
            obj["lastname"] = exists[2]
            obj["department"] = exists[3]
            return jsonify(obj)
        else:
            raise Exception
    except Exception as e:
        return jsonify({"detail":"Student data not found"})


@app.route("/update/student/<id>", methods=["PUT"])
def update_student(id):
    try:
        sqlite = sqlite3.connect("student.db")
        db = sqlite.cursor()
        student = Student(request.json["firstname"],
                      request.json["lastname"],
                      request.json["department"]
                      )
        db.execute('''UPDATE STUDENTS SET firstname = ?, lastname =?, department =? WHERE id=?''',
              (student.f_name, student.l_name, student.department, id))
        sqlite.commit()
        return jsonify({"detail":"student data updated successfully"})
    except Exception as e:
        print(e)

@app.route("/delete/student/<id>", methods=["DELETE"])
def delete_student(id):
    try:
        sqlite = sqlite3.connect("student.db")
        db = sqlite.cursor()
        exists = db.execute('''SELECT * FROM STUDENTS WHERE id=?''', (id,)).fetchone()
        if exists is not None:
            db.execute('''DELETE FROM STUDENTS WHERE id=?''', (id,))
        else: 
            raise Exception
        sqlite.commit()
        return jsonify({"detail":"Student data deleted successfully"})
    except Exception as e:
        return jsonify({"detail":"Student data not found"})




if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"), debug=True)