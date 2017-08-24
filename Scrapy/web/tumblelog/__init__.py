from flask import Flask
from flask_mongoengine import MongoEngine,MongoEngineSessionInterface
from flask_mail import Mail, Message

app = Flask(__name__)
#maybe from the file
#app.config.from_pyfile('the-config.cfg')
app.config['MONGODB_SETTINGS'] = {
    'db': 'dbtest'
    ,'username':'admin'
    ,'password':'sa'
    ,'host':'localhost'
    ,'port':27017
}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

app.session_interface = MongoEngineSessionInterface(db)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_USERNAME'] = 'thassange@163.com'
app.config['MAIL_PASSWORD'] = 'thassange163'

mail = Mail(app)

mailComm = {
            "mail": mail
            ,"message": Message
        }

def register_blueprints(app):
    # Prevents circular imports
    from tumblelog.views import posts
    from tumblelog.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
