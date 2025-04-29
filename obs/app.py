from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def anasayfa():
    return render_template("anasayfa.html")



@app.route("/giriş")
def giris():
    return render_template("giriş.html")

@app.route("/kayit")
def kayit():
    return render_template("kayit.html")








if __name__ == "__main__":
    app.run(debug=True)