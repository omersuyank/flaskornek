from flask import Blueprint, request, jsonify
import pyodbc

service_controller = Blueprint('service_controller', __name__)

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=104.247.167.130\\mssqlserver2022;"
    "DATABASE=veritabanı_adı;"
    "UID=veritabanı_adı;"
    "PWD=veritabanı_şifresi"
)


@service_controller.route('/add_service', methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        required_fields = ['name', 'description', 'service_code','short_description','photo_url','is_active']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli alanlar eksik"}), 400

        name = data['name']
        description = data['description']
        service_code = data['service_code']
        short_description = data['short_description']
        photo_url = data['photo_url']
        is_active = data['is_active']


        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO TblService (name, description, service_code, is_active,short_description,photo_url) VALUES (?, ?, ?, ?,?,?)",
                (name, description, service_code,is_active,short_description,photo_url)
            )
            db.commit()

        return jsonify({"message": "Servis başarıyla eklendi!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@service_controller.route('/get_services/<status>', methods=['GET'])
def get_services(status):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            if status=="all":
                cursor.execute("SELECT * FROM TblService")
            else:
                cursor.execute("SELECT * FROM TblService WHERE is_active=?",(status))
            rows = cursor.fetchall()

            services = []
            for row in rows:
                service = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "service_code": row[3],
                    "is_active": row[4],
                    "short_description": row[5],
                    "photo_url": row[6],
                }
                services.append(service)

        return jsonify({"services":services}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@service_controller.route('/get_service/<int:service_id>', methods=['GET'])
def get_service(service_id):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM TblService WHERE id=? ", (service_id,))
            row = cursor.fetchone()
            print(row)
            if row:
                service = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "service_code": row[3],
                    "is_active": row[4],
                    "short_description": row[5],
                    "photo_url": row[6],
                }
                return jsonify({"services":service}), 200
            else:
                return jsonify({"error": "Servis bulunamadı!"}), 404

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@service_controller.route('/update_service/<int:service_id>', methods=['POST'])
def update_service(service_id):
    try:
        data = request.get_json()
        print(data)
        required_fields = ['name', 'description', 'service_code','short_description','photo_url','is_active']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli alanlar eksik"}), 400

        name = data['name']
        description = data['description']
        service_code = data['service_code']
        short_description = data['short_description']
        photo_url = data['photo_url']
        is_active = data['is_active']

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE TblService SET name=?, description=?, service_code=?, short_description=?,photo_url=?,is_active=? WHERE id=?",
                (name, description, service_code,short_description,photo_url,is_active, service_id)
            )
            if cursor.rowcount == 0:
                return jsonify({"error": "Servis bulunamadı veya güncellenemedi!"}), 404

            db.commit()

        return jsonify({"message": "Servis başarıyla güncellendi!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@service_controller.route('/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM TblService WHERE id = ?", (service_id,))

            if cursor.rowcount == 0:
                return jsonify({"error": "Servis bulunamadı veya zaten silinmiş!"}), 404

            db.commit()

        return jsonify({"message": "Servis başarıyla silindi (pasif hale getirildi)!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500


@service_controller.route('/update_service_is_active/<int:service_id>', methods=['POST'])
def update_service_is_active(service_id):
    try:
        data = request.get_json()
        print(f"Gelen İstek: {data}")  # Terminalde ne geldiğini görmek için

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("SELECT id,is_active FROM TblService WHERE id = ?", (service_id,))
            row = cursor.fetchone()
            print(row)
            if row[1]==1:
                cursor.execute(
                    "UPDATE TblService SET is_active=0 WHERE id=? ",
                    (service_id,)
                )
            else:
                cursor.execute(
                    "UPDATE TblService SET is_active=1 WHERE id=? ",
                    (service_id,)
                )

            if cursor.rowcount == 0:
                return jsonify({"error": "Servis bulunamadı veya güncellenemedi!"}), 404

            db.commit()

        return jsonify({"message": "Servis başarıyla güncellendi!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500
