from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from openai import OpenAI
import os
import time

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize an empty chat history
chat_history = []


@app.route("/")
def model():
    return render_template("model_selection.html")


@app.route("/upload", methods=["POST"])
def handle_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        # Save the file as credentials.json
        filename = "credentials.json"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400


def allowed_file(filename):
    # Check for allowed file extensions
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"json"}


@app.route("/screen2")
def screen2():
    return render_template("screen2.html")


@app.route("/generate", methods=["POST"])
def generate():
    model_type = session.get("model_type")
    system_prompt = request.form["system_prompt"]
    user_prompt = request.form["user_prompt"]

    # Append the current conversation to the chat history
    chat_history[0]["system"] = system_prompt

    if model_type.contains("dgpt"):
        return call_gpt_model(user_prompt, chat_history)
    elif model_type.contains("claude-3"):
        return call_claude_3_model(user_prompt, chat_history)

    client = OpenAI(api_key="OPENAI_API_KEY")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})

    return jsonify({"assistant_response": assistant_response})


def call_gpt_model(user_prompt, chat_history):
    openai_api_key = request.form["api-key-input"]
    # model = request.form["model-input"]
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=chat_history,
        temperature=0.7,
        max_tokens=4096,
    )

    assistant_response = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": assistant_response})


def call_claude_3_model(user_prompt, chat_history):
    return jsonify({"error": "Not implemented"})


if __name__ == "__main__":
    app.run(debug=True)
