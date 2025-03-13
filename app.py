import json
import os
from file_utilities import frequency_from_hash, length_from_hash, save_upload
import parser
import sys

from bottle import Bottle, request, response, run, static_file, template

dirname = os.path.dirname(sys.argv[0])

app = Bottle()


@app.route("/static/<filename:re:.*.ico>")
def send_ico(filename):
    return static_file(filename, root=dirname + "/static/asset/")


@app.route("/static/<filename:re:.*.css>")
def send_css(filename):
    return static_file(filename, root=dirname + "/static/asset/css")


@app.route("/static/<filename:re:.*.js>")
def send_js(filename):
    return static_file(filename, root=dirname + "/static/asset/js")


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


@app.post("/upload")
def upload_file():

    upload = request.files.get("file")

    if not upload:
        response.status = 400
        return {"error": "No file uploaded"}

    return save_upload(upload)


@app.route("/")
@app.get("/upload")
def serve_upload_page():
    return template("upload")


if __name__ == "__main__":

    run(app, host="localhost", port=8000, debug=True, reloader=True)
