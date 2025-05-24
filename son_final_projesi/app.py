from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geliştirme_anahtarı_12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veritabani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'giriş'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def anasayfa2():
    return render_template("anasayfa2.html")


@app.route('/ayarlar')
@login_required
def ayarlar():
    return render_template("ayarlar.html")


@app.route('/dersler')
@login_required
def dersler():
    return render_template("dersler.html")


@app.route('/giriş', methods=['GET', 'POST'])
def giriş():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('anasayfa'))
        else:
            flash('Geçersiz e-posta veya şifre.', 'danger')
    return render_template("giriş.html")

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('kayit'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('giriş'))
    return render_template("kayit.html")

@app.route('/ogrenciler')
@login_required
def ogrenciler():

    return render_template("ogrenciler.html", ogrenciler=ogrenciler)


@app.route('/notlar')
@login_required
def notlar():
    return render_template("notlar.html")


@app.route('/raporlar')
@login_required
def raporlar():
    return render_template("raporlar.html")


@app.route('/admin')
@login_required
def admin_panel():
    return render_template("admin.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('anasayfa'))

@app.route('/anasayfa')
@login_required
def anasayfa():
    return render_template("anasayfa.html")




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
    
    
