import glob
import hashlib
import os


import parser

UPLOAD_FOLDER = "uploads"


def get_files_from_hashes(file_hashes):

    files = glob.glob("uploads/*")
    datas = []
    for file_hash in file_hashes:
        for file_path in files:
            if file_hash in file_path:
                break
            file_path = None

        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = file.read()
                    datas.append(data)
                except UnicodeDecodeError as _:
                    pass

    return datas


def root_file_name_from_hash(file_hash):
    files = glob.glob("uploads/*")

    for file_path in files:
        if file_hash in file_path:
            root = os.path.basename(file_path).replace(f"-{file_hash}", "")

            return root


def frequency_from_hashes(file_hashes, sort_option):
    datas = get_files_from_hashes(file_hashes)
    frequencys = []
    for data in datas:

        frequencys.extend(parser.HtmlParser(data).get_frequencys(sort_option))
    return frequencys


def compute_file_hash(file):
    """Compute SHA-256 hash of an uploaded file"""
    hasher = hashlib.sha256()

    for chunk in iter(lambda: file.read(4096), b""):  # Read in chunks
        hasher.update(chunk)
    file.seek(0)  # Reset file pointer
    return hasher.hexdigest()


def length_from_hashes(file_hashes, grouped):
    datas = get_files_from_hashes(file_hashes)

    length_dict = dict()

    for data in datas:
        data_lengths = parser.HtmlParser(data).get_length_counts(grouped)

        for key in data_lengths:
            if key in length_dict:
                length_dict[key] += length_dict[key] + data_lengths[key]
            else:
                length_dict[key] = data_lengths[key]

    return {"labels": list(length_dict.keys()), "data": list(length_dict.values())}


def save_upload(upload):
    # Compute the hash of the saved file
    file_hash = compute_file_hash(upload.file)

    file_path = os.path.join(UPLOAD_FOLDER, upload.filename + "-" + file_hash)

    # Save the uploaded file to the specified directory
    try:
        if not os.path.exists(file_path):
            upload.save(file_path)

        # Return the file hash as JSON response
        return {"hash": file_hash, "filename": upload.filename}

    except Exception as e:

        return {"error": f"Server error: {str(e)}"}
