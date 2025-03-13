import csv
import json
import os

from matplotlib import pyplot as plt
import parser
import sys

from bottle import Bottle, request, response, run, static_file, template

from file_utilities import (
    frequency_from_hash,
    length_from_hash,
    root_file_name_from_hash,
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


@app.route("/length")
def length():

    data = {"test": "Hello this is a length"}
    return template("length", data=data)


@app.route("/length-data")
def chart_data():

    file_hash = request.query.get("hash")
    grouped_selection = request.query.get("grouped")
    grouped = True if grouped_selection == "true" else False

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


@app.route("/download")
def download_file():

    page = request.query.get("page")
    file_hash = request.query.get("hash")
    print(f"{page=} {file_hash=}")
    if not file_hash:
        return
    if page == "frequency":

        sort_order = request.query.get("file_hash")

        sort_order_map = {
            "frequency": parser.SortOptions.FREQUENCY,
            "reverse-frequency": parser.SortOptions.REVERSE_FREQUENCY,
            "alphabetical": parser.SortOptions.ALPHABETICAL,
            "reverse-alphabetical": parser.SortOptions.REVERSE_ALPHABETICAL,
        }

        sort_option = (
            sort_order_map[sort_order] if sort_order else parser.SortOptions.FREQUENCY
        )
        root_file_name = root_file_name_from_hash(file_hash)
        print(f"{root_file_name=}")
        frequency = frequency_from_hash(file_hash, sort_option)

        file_path = f"{root_file_name}_frequency.csv"
        with open(f"output/{file_path}", "w", encoding="utf-8") as file:
            file_writer = csv.writer(file, delimiter=",")
            for line in frequency:
                file_writer.writerow(line)

        response.headers["Content-Disposition"] = response.headers[
            "Content-Disposition"
        ] = "attachment"

        return static_file(file_path, root="./output", download=True)
    elif page == "lengths":
        grouped_selection = request.query.get("grouped")
        grouped = True if grouped_selection == "true" else False

        if file_hash:
            word_data = length_from_hash(file_hash, grouped)
        else:
            word_data = {"labels": [], "data": []}

        root_file_name = root_file_name_from_hash(file_hash)
        file_path = f"{root_file_name}_lengths.png"

        plt.bar(word_data["labels"], word_data["data"])
        plt.savefig(f"./output/{file_path}")

        response.headers["Content-Disposition"] = response.headers[
            "Content-Disposition"
        ] = "attachment"

        return static_file(file_path, root="./output", download=True)


if __name__ == "__main__":

    run(app, host="localhost", port=8000, debug=True, reloader=True)
