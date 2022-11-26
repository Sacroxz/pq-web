from flask import Flask, render_template
# import oracledb

app = Flask(__name__)

# connection = cx_Oracle.connect(user="admin", password="x52JjUGZrTa8VZw", dsn="ehuurlu4scvu47zv_low", encoding="UTF-8")
# connection = oracledb.connect(user="admin", password="x52JjUGZrTa8VZw", dsn="ehuurlu4scvu47zv_high", config_dir="opt/config", wallet_location="opt/config", wallet_password="x52JjUGZrTa8VZw", encoding="UTF-8")
# print("Database version:", connection.version)

@app.route("/")
def home():
    return render_template("home.html")

# TODO: Add post logic.
# @app.route("/post", methods=["POST"])
# def post_cuidados():
#     return render_template("post.html")

if __name__ == '__main__':
    app.run()