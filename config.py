from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = (
    "mssql+pyodbc://huseyi98_UykaTechAPI:T*a8z54p5"
    "@104.247.167.130\\mssqlserver2022"
    "/huseyi98_UykaTechAPI"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=yes"
)

db = SQLAlchemy()
