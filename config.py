from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = (
    "mssql+pyodbc://veritabanı_adı:veritabanı_şifresi"
    "@104.247.167.130\\mssqlserver2022"
    "/veritabanı_adı"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=yes"
)

db = SQLAlchemy()
