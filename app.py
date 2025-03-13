import hashlib
import json
import os
import parser
import sys

import bottle
from bottle import Bottle, request, response, run, static_file, template

dirname = os.path.dirname(sys.argv[0])

app = Bottle()
UPLOAD_FOLDER = "uploads"


@app.route("/static/<filename:re:.*.ico>")
def send_ico(filename):
    return static_file(filename, root=dirname + "/static/asset/")


@app.route("/static/<filename:re:.*.css>")
def send_css(filename):
    return static_file(filename, root=dirname + "/static/asset/css")


@app.route("/static/<filename:re:.*.js>")
def send_js(filename):
    return static_file(filename, root=dirname + "/static/asset/js")


def get_file_from_hash(file_hash):
    file_path = os.path.join(UPLOAD_FOLDER, file_hash)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = file.read()
            except UnicodeDecodeError as e:
                return "File could not be decoded!", 404

        return data
    return "File not found!", 404


def frequency_from_hash(file_hash, sort_option):
    data = get_file_from_hash(file_hash)

    return parser.HtmlParser(data).get_frequencys(sort_option)


def length_from_hash(file_hash, grouped):
    data = get_file_from_hash(file_hash)

    return parser.HtmlParser(data).get_length_counts(grouped)


@app.route("/frequency")
def frequency():

    sort_order = request.query.get("sort_order")
    file_hash = request.query.get("hash")

    sort_order_map = {
        "frequency": parser.SortOptions.FREQUENCY,
        "reverse-frequency": parser.SortOptions.REVERSE_FREQUENCY,
        "alphabetical": parser.SortOptions.ALPHABETICAL,
        "reverse-alphabetical": parser.SortOptions.REVERSE_ALPHABETICAL,
    }

    sort_option = (
        sort_order_map[sort_order] if sort_order else parser.SortOptions.FREQUENCY
    )
    print(sort_option)
    if file_hash:
        frequency = frequency_from_hash(file_hash, sort_option)
    else:
        frequency = []

    data = {
        "words": [i[0] for i in frequency],
        "frequency": [i[1] for i in frequency],
    }

    return template("frequency", data=data, root=dirname + "/veiws")


grouped = False


@app.route("/length")
def length():
    grouped_selection = request.query.get("grouped")

    global grouped
    grouped = True if grouped_selection == "true" else False

    data = {"test": "Hello this is a length"}
    return template("length", data=data)


@app.route("/length-data")
def chart_data():

    file_hash = request.query.get("hash")
    grouped = request.query.get("grouped")

    if file_hash:
        word_data = length_from_hash(file_hash, grouped)
    else:
        word_data = {"labels": [], "data": []}
    data = {
        "labels": word_data["labels"],
        "datasets": [
            {
                "label": "Word lengths",
                "data": word_data["data"],
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            }
        ],
    }
    response.content_type = "application/json"

    return json.dumps(data)


def compute_file_hash(file):
    """Compute SHA-256 hash of an uploaded file"""
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):  # Read in chunks
        hasher.update(chunk)
    file.seek(0)  # Reset file pointer
    return hasher.hexdigest()


@app.post("/upload")
def upload_file():
    """Handle file upload and return its hash"""
    upload = request.files.get("file")

    print(upload)
    if not upload:
        response.status = 400
        return {"error": "No file uploaded"}

    # Compute the hash of the saved file
    file_hash = compute_file_hash(upload.file)

    file_path = os.path.join(UPLOAD_FOLDER, file_hash)

    # Save the uploaded file to the specified directory
    try:
        if not os.path.exists(file_path):
            upload.save(file_path)

        # Return the file hash as JSON response
        return {"hash": file_hash}

    except Exception as e:
        response.status = 500
        return {"error": f"Server error: {str(e)}"}


@app.route("/")
@app.get("/upload")
def serve_upload_page():
    return template("upload")


if __name__ == "__main__":

    run(app, host="localhost", port=8000, debug=True, reloader=True)
