from flask import Blueprint, request, jsonify
import pyodbc
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import datetime
import bcrypt

session_controller = Blueprint('session_controller', __name__)

SECRET_KEY = "FRUU9V!?->u7sb%Vo0CL&<JrRttq&E9u#<mr4Qtaw1WS9xCfc?P+m/HrWFc@9&HZ"

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=104.247.167.130\\mssqlserver2022;"
    "DATABASE=huseyi98_UykaTechAPI;"
    "UID=huseyi98_UykaTechAPI;"
    "PWD=T*a8z54p5"
)




@session_controller.route('/register', methods=['POST'])
def register_user():
    try:
        # JSON verisini al
        data = request.get_json()
        print("Gelen JSON:", data)  # JSON verisini yazdır

        # Gerekli alanları kontrol et
        required_fields = ['name', 'surname', 'email', 'phone', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        # Alanları al
        name = data['name']
        surname = data['surname']
        email = data['email']
        phone = data['phone']
        password = data['password'].encode('utf-8')  # Şifreyi encode et

        # Şifreyi bcrypt ile hashle
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        # Veritabanı bağlantısı
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()

            # Aynı e-posta veya telefon numarasıyla kayıtlı kullanıcı olup olmadığını kontrol et
            cursor.execute("SELECT email, phone FROM TblUser WHERE email = ? OR phone = ?", (email, phone))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user[0] == email:
                    return jsonify({"error": "Bu e-posta zaten kayitli!"}), 400

            # Yeni kullanıcıyı ekle
            cursor.execute(
                "INSERT INTO TblUser (name, surname, email, phone, password, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                (name, surname, email, phone, hashed_password)
            )
            db.commit()

        return jsonify({"message": "Kullanıcı başarıyla eklendi!"}), 200

    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500



@session_controller.route('/login', methods=['POST'])
def login():
    """Mail ve şifre ile giriş yapar ve statü bilgisini döner."""
    try:
        data = request.get_json()
        print("Gelen JSON:", data)

        if not all(k in data for k in ('email', 'password')):

            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        email = data['email']
        password = data['password'].encode('utf-8')

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, name, surname, password FROM TblUser WHERE email = ? AND is_active = 1",
                (email,)
            )
            result = cursor.fetchone()

        if result:
            user_id, name, surname, hashed_password = result
            hashed_password = hashed_password.encode('utf-8')

            if bcrypt.checkpw(password, hashed_password):
                payload = {
                    "user_id": user_id,
                    "name": name,
                    "surname": surname,
                    "email":email,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

                return jsonify({
                    "message": "Giriş başarılı!",
                    "token": token
                }), 200
            else:
                return jsonify({"error": "Geçersiz e-posta veya şifre"}), 401
        else:
            return jsonify({"error": "Geçersiz e-posta veya şifre"}), 401

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500



