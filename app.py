from bs4.diagnose import profile
from flask import Flask
from flask_migrate import Migrate
from jupyter_core.migrate import migrate
from flask_cors import CORS


"""
from config import db, DATABASE_URI
from models.TblAdmin import Admin
from models.TblTeam import Team
from models.TblAbout import About
from models.TblService import Service
from models.TblPackages import Package
from models.TblUser import User
from models.TblSocialMedia import SocialMedia
from models.TblContactMessages import ContactMessages
from models.TblBlog import Blog
"""


from controllers.UserController import user_controller
from controllers.SessionController import session_controller
from controllers.AdminController import admin_controller
from controllers.BlogController import blog_controller
from controllers.TeamController import team_controller
from controllers.MailController import mail_controller
from controllers.ServiceController import service_controller

app = Flask(__name__)
#migrate = Migrate(app,db)
CORS(app)

"""
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
"""

app.register_blueprint(user_controller, url_prefix='/User')
app.register_blueprint(session_controller, url_prefix='/Session')
app.register_blueprint(admin_controller, url_prefix='/Admin')
app.register_blueprint(team_controller, url_prefix='/Team')
app.register_blueprint(blog_controller, url_prefix='/Blog')
app.register_blueprint(mail_controller, url_prefix='/Mail')
app.register_blueprint(service_controller, url_prefix='/Service')





@app.route('/')
def home():
    return "Flask API Çalışıyor!", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
