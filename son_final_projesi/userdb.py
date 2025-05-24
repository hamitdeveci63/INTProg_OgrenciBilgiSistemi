from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veritabani.db'
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    
def to_join():
    with app.app_context():
        users = User.query.all()
        data =[]
        for user in users:
            data.append({
                'id':user.id,
                'name':user.name,
                'username':user.username,
                'email':user.email,
                'password':user.password
            })
        with open('user.json','w',encoding='utf-8') as dosya:
            json.dump(data,dosya,ensure_ascii=False,indent=5)
        print("json dosyasına aktarım başarılı")

if __name__ == '__main__':
    to_join()