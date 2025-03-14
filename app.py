import csv
import json
import os

from matplotlib import pyplot as plt
import parser
import sys

from bottle import Bottle, request, response, run, static_file, template

from file_utilities import (
    frequency_from_hashes,
    length_from_hashes,
    save_upload,
)

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
    file_hashes = request.query.get("hashes")
    if not file_hashes:
        return template(
            "frequency",
            data={"words": [], "frequency": []},
            SERVER_URL=SERVER_URL,
            root=dirname + "/veiws",
        )

    file_hashes = file_hashes.split(",")

    sort_order_map = {
        "frequency": parser.SortOptions.FREQUENCY,
        "reverse-frequency": parser.SortOptions.REVERSE_FREQUENCY,
        "alphabetical": parser.SortOptions.ALPHABETICAL,
        "reverse-alphabetical": parser.SortOptions.REVERSE_ALPHABETICAL,
    }

    sort_option = (
        sort_order_map[sort_order] if sort_order else parser.SortOptions.FREQUENCY
    )

    frequency = frequency_from_hashes(file_hashes, sort_option) if file_hashes else []

    data = {
        "words": [i[0] for i in frequency],
        "frequency": [i[1] for i in frequency],
    }

    return template(
        "frequency", data=data, SERVER_URL=SERVER_URL, root=dirname + "/veiws"
    )


@app.route("/length")
def length():
    data = {
        "test": "Hello this is a length",
    }
    return template("length", data=data, SERVER_URL=SERVER_URL)


@app.route("/length-data")
def chart_data():
    file_hashes = request.query.get("hashes").split(",")
    grouped_selection = request.query.get("grouped")
    grouped = True if grouped_selection == "true" else False

    word_data = (
        length_from_hashes(file_hashes, grouped)
        if file_hashes
        else {"labels": [], "data": []}
    )

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
    return data


@app.post("/upload")
def upload_file():
    uploaded_files = request.files.getall("files")  # Get multiple files
    file_data = {"hashes": [], "filenames": []}
    for upload in uploaded_files:
        if not upload:
            pass

        result = save_upload(upload)
        if "error" not in result:
            file_data["hashes"] = file_data["hashes"] + [result["hash"]]
            file_data["filenames"] = file_data["filenames"] + [result["filename"]]

    response.content_type = "application/json"

    return json.dumps(file_data)


@app.route("/")
@app.get("/upload")
def serve_upload_page():
    hashes = request.query.getall("hash")  # Retrieve hashes from URL

    return template("upload", file_hashes=hashes, SERVER_URL=SERVER_URL)


def create_frequency_output(file_hashes):
    sort_option = parser.SortOptions.FREQUENCY

    root_file_name = "output"
    frequency = frequency_from_hashes(file_hashes, sort_option)

    file_path = f"{root_file_name}_frequency.csv"
    with open(f"output/{file_path}", "w", encoding="utf-8") as file:
        file_writer = csv.writer(file, delimiter=",")
        for line in frequency:
            file_writer.writerow(line)

    response.headers["Content-Disposition"] = response.headers[
        "Content-Disposition"
    ] = "attachment"

    return static_file(file_path, root="./output", download=True)


def create_lengths_output(file_hashes):
    grouped_selection = request.query.get("grouped")
    grouped = True if grouped_selection == "true" else False

    word_data = (
        length_from_hashes(file_hashes, grouped)
        if file_hashes
        else {"labels": [], "data": []}
    )

    file_path = "output_lengths.png"

    plt.bar(word_data["labels"], word_data["data"])
    plt.savefig(f"./output/{file_path}")

    response.headers["Content-Disposition"] = response.headers[
        "Content-Disposition"
    ] = "attachment"

    return static_file(file_path, root="./output", download=True)


@app.route("/download")
def download_file():
    page = request.query.get("page")
    file_hashes = request.query.get("hashes")

    if not file_hashes:
        return
    file_hashes = file_hashes.split(",")

    if page == "frequency":
        return create_frequency_output(file_hashes)

    elif page == "lengths":
        return create_lengths_output(file_hashes)


if __name__ == "__main__":
    PORT = os.environ.get("PORT", "8000")
    SERVER = os.environ.get("SERVER", "false")
    if SERVER == "false":
        SERVER_URL = f"http://localhost:{PORT}"
        run(app, host="localhost", port=int(PORT), debug=True, reloader=True)
    else:
        SERVER_URL = "https://webpageparser.onrender.com"
        run(app, host="0.0.0.0", port=int(PORT), debug=True, reloader=True)
