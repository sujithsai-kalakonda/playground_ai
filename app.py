from flask import Flask, render_template, request, redirect, url_for
import os
import time

app = Flask(__name__)

# Ensure the 'uploads' folder exists
uploads_dir = os.path.join(app.instance_path, "uploads")
os.makedirs(uploads_dir, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    # get the uploaded file
    file = request.files["file"]

    # save the file to a folder named 'uploads' in the current directory
    file.save(os.path.join(uploads_dir, file.filename))

    # Redirect to the next screen
    return redirect(url_for("screen2"))


@app.route("/screen2")
def screen2():
    return "Screen 2"


if __name__ == "__main__":
    app.run(debug=True)
