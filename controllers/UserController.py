from flask import Blueprint,request,jsonify
import pyodbc
import os
import base64
from werkzeug.utils import secure_filename
import bcrypt

user_controller = Blueprint('user_controller',__name__)


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=104.247.167.130\\mssqlserver2022;"
    "DATABASE=huseyi98_UykaTechAPI;"
    "UID=huseyi98_UykaTechAPI;"
    "PWD=T*a8z54p5"
)

UPLOAD_FOLDER = "uploads/profile_images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_controller.route('/update_user/<int:id>',methods = ['POST'])
def update_user(id):
    try:
        data=request.get_json()
        print("Gelen JSON",data)

        required_fields = ['name', 'surname', 'email', 'phone']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400


        name = data["name"]
        surname = data["surname"]
        email = data["email"]
        phone = data["phone"]


        with pyodbc.connect(CONNECTION_STRING) as db:

            cursor = db.cursor()
            cursor.execute(
                "UPDATE TblUser SET name = ?, surname = ?, email = ?, phone = ? WHERE id=?",
                (name, surname, email, phone,id)
            )
            db.commit()

        return jsonify({"message":"Kullanıcı başarıyla güncellendi"}), 200
    except KeyError as e:
        print(f"KeyError:{e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@user_controller.route('/update_password',methods= ['POST'])
def update_password():

    try:
        data = request.get_json()
        print("Gelen JSON",data)

        required_fields = ['id','password']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        id = data["id"]
        password = data['password'].encode('utf-8')

        # Yeni şifreyi bcrypt ile hashle
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        with pyodbc.connect(CONNECTION_STRING) as db:

            cursor = db.cursor()
            cursor.execute(
                "UPDATE TblUser SET password = ?  WHERE id=?",
                (hashed_password,id)
            )
            db.commit()

        return jsonify({"message": "Şifreniz başarıyla güncellendi!"}), 200
    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@user_controller.route('/get_users', methods=['GET'])
def get_users():
    """Tüm kullanıcıları listeler ve her kullanıcı için profil fotoğrafını döndürür."""
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()

            # Tüm kullanıcıları çek
            cursor.execute("SELECT id, name, surname, email, phone, is_active,photo_url FROM TblUser")
            rows = cursor.fetchall()


        users = []
        for row in rows:

            user_id = row[0]
            user = {
                "id": user_id,
                "name": row[1],
                "surname": row[2],
                "email": row[3],
                "phone": row[4],
                "is_active": row[5],
                "profile_img_path":row[6]
            }




            users.append(user)

        return jsonify(users), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@user_controller.route('/get_user_by_id/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("SELECT name, surname, email, phone, is_active,photo_url FROM TblUser WHERE id = ?", (id,))
            row = cursor.fetchone()



        if row:

            user = {
                "id": id,
                "name": row[0],
                "surname": row[1],
                "email": row[2],
                "phone": row[3],
                "is_active": row[4],
                "profile_img_path": row[5]
            }
            return jsonify(user), 200
        else:
            return jsonify({"error": "Kullanıcı bulunamadı"}), 404

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500