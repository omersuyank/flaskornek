
from flask import Blueprint, request, jsonify
import pyodbc


blog_controller = Blueprint('blog_controller', __name__)

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=104.247.167.130\\mssqlserver2022;"
    "DATABASE=veritabanı_adı;"
    "UID=veritabanı_adı;"
    "PWD=veritabanı_şifresi"
)

@blog_controller.route('/add_blog_content', methods=['POST'])
def add_blog_content():
    try:
        # JSON verisini al
        data = request.get_json()
        print("Gelen JSON:", data)  # JSON verisini yazdır

        # Gerekli alanları kontrol et
        required_fields = ['title', 'content', 'image_path']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        # Alanları al
        title = data['title']
        content = data['content']

        image_path = data['image_path']


        # Veritabanı bağlantısı
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()

            # Yeni içerik ekle
            cursor.execute(
                "INSERT INTO TblBlog (title,content,created_at,image_path,is_active) VALUES (?, ?, GETDATE(), ?, 1)",
                (title, content, image_path)
            )
            db.commit()

        return jsonify({"message": "Içerik başarıyla eklendi!"}), 200

    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@blog_controller.route('/get_blog_contents', methods=['GET'])
def get_blog_contents():
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM TblBlog WHERE is_active=1")
            rows = cursor.fetchall()
            blog_contents=[]
            for row in rows:

                blog_content={
                    "id":row[0],
                    "title":row[1],
                    "content":row[2],
                    "created_at":row[3].strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "image_path":row[4]


                }
                blog_contents.append(blog_content)

        return jsonify(blog_contents), 200

    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@blog_controller.route('/get_blog_content/<int:content_id>', methods=['GET'])
def get_blog_content(content_id):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM TblBlog WHERE id=? AND is_active=1",(content_id))
            row = cursor.fetchone()

            blog_content={
                "id":row[0],
                "title":row[1],
                "content":row[2],
                "created_at":row[3].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "image_path":row[4],
                "is_active":row[5]
            }

 
        return jsonify({"blog_content":blog_content}), 200

    except KeyError as e:
        print(f"KeyError: {e}")
        return jsonify({"error": f"Eksik anahtar: {str(e)}"}), 400
    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@blog_controller.route('/get_blog_content_by_status/<contentType>', methods=['GET'])
def get_blog_content_by_status(contentType):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()
            print(f"İstek Alındı: {contentType}")

            if contentType == "all":
                cursor.execute("SELECT * FROM TblBlog")
            else:
                cursor.execute("SELECT * FROM TblBlog WHERE is_active=?", (contentType,))

            rows = cursor.fetchall()

            # Eğer hiçbir sonuç dönmezse 404 döndür
            if not rows:
                return jsonify({"error": "Blog içeriği bulunamadı"}), 404

            # JSON formatına çevir
            blog_contents = []
            for row in rows:
                blog_contents.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "created_at": row[3].strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "image_path": row[4],
                    "is_active": row[5]
                })

        # Yanıtı konsolda görmek için yazdır
        print("API Yanıtı:", blog_contents)

        return jsonify({"blog_contents": blog_contents}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@blog_controller.route('/delete_blog_content/<int:content_id>', methods=['POST'])
def delete_blog_content(content_id):
    try:
        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()

            # İçeriğin olup olmadığını kontrol et
            cursor.execute("SELECT * FROM TblBlog WHERE id = ?", (content_id,))
            content = cursor.fetchone()
            if not content:
                return jsonify({"error": "Blog içeriği bulunamadı"}), 404

            # Silme işlemi (soft delete - is_active = 0)
            cursor.execute("UPDATE TblBlog SET is_active = 0 WHERE id = ?", (content_id,))
            db.commit()

        return jsonify({"message": "Blog içeriği başarıyla silindi!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

@blog_controller.route('/update_blog_content/<int:content_id>', methods=['PUT'])
def update_blog_content(content_id):
    try:
        data = request.get_json()
        print("Gelen JSON:", data)  # JSON verisini yazdır

        required_fields = ['title', 'content', 'image_path']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Gerekli anahtarlar eksik"}), 400

        title = data['title']
        content = data['content']
        image_path = data['image_path']

        with pyodbc.connect(CONNECTION_STRING) as db:
            cursor = db.cursor()

            # İçeriğin olup olmadığını kontrol et
            cursor.execute("SELECT * FROM TblBlog WHERE id = ?", (content_id,))
            blog_content = cursor.fetchone()
            if not blog_content:
                return jsonify({"error": "Blog içeriği bulunamadı"}), 404

            # Güncelleme işlemi
            cursor.execute(
                "UPDATE TblBlog SET title=?, content=?, image_path=? WHERE id=?",
                (title, content, image_path, content_id)
            )
            db.commit()

        return jsonify({"message": "Blog içeriği başarıyla güncellendi!"}), 200

    except pyodbc.Error as e:
        print(f"MSSQL Hatası: {e}")
        return jsonify({"error": "Veritabanı Hatası"}), 500
    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"error": "Dahili Sunucu Hatası"}), 500

