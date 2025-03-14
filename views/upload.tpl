<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Drag & Drop File Upload</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <style>
      .drop-zone {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        color: #007bff;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      .drop-zone.dragover {
        background-color: #f0f8ff;
      }
    </style>
  </head>
  <body class="bg-light">
    <nav class="navbar navbar-default navbar-static-top">
      <ul
        class="nav nav-tabs flex-column flex-sm-row nav-fill"
        style="width: 95%"
      >
        <li class="nav-item">
          <a
            class="nav-link active"
            aria-current="page"
            href="upload"
            id="uploadLink"
            >Upload</a
          >
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            href="frequency?order=frequency"
            id="frequencyLink"
            >Word Frequency</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" href="length" id="lengthLink">Word Lengths</a>
        </li>
      </ul>
    </nav>
    <!-- The drop-zone and upload UI -->

    <div class="card shadow p-4" style="width: 60%; height: 30%; margin: auto">
      <h2 class="mb-3 text-center">Drag & Drop File Upload</h2>

      <!-- Drag & Drop Zone -->
      <div id="dropZone" class="drop-zone">
        Drag & Drop a file here or
        <span class="text-primary">click to select</span>
        <input type="file" id="fileInput" class="d-none" multiple />
      </div>

      <!-- Upload Button -->

      <div id="hashDisplay" class="alert alert-success mt-3 d-none">
        <strong>File Uploaded:</strong> <span id="fileName"></span>
      </div>
    </div>
    <script>
      const dropZone = document.getElementById("dropZone");
      const fileInput = document.getElementById("fileInput");
      let selectedFiles = [];

      // Handle Drag Over
      dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropZone.classList.add("dragover");
      });

      dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
      });

      // Handle File Drop
      dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        dropZone.classList.remove("dragover");

        if (event.dataTransfer.files.length > 0) {
          selectedFiles = Array.from(event.dataTransfer.files);
          updateFileList();
          uploadFiles();
        }
      });

      // Handle Click to Select File
      dropZone.addEventListener("click", () => {
        fileInput.click();
      });

      fileInput.addEventListener("change", (event) => {
        if (event.target.files.length > 0) {
          selectedFiles = Array.from(event.target.files);
          updateFileList();
          uploadFiles();
        }
      });

      // Function to update file list display
      function updateFileList() {
        dropZone.innerHTML =
          selectedFiles
            .map((file) => `<strong>${file.name}</strong>`)
            .join(", ") + " selected";
      }

      // Handle File Upload
      async function uploadFiles() {
        if (selectedFiles.length === 0) return alert("No files selected!");

        const formData = new FormData();
        selectedFiles.forEach((file) => formData.append("files", file));

        try {
          // Make the upload request to the correct port (8000)
          const response = await fetch(
            "https://webpageparser.onrender.com/upload",
            {
              method: "POST",
              body: formData,
            }
          );

          // Check if response was successful
          if (response.ok) {
            const data = await response.json();
            console.log(data);

            updateNavLinks(data.hashes); // Use the first file's hash for navigation

            document.getElementById("hashDisplay").classList.remove("d-none");

            // Display uploaded file names and hashes
            document.getElementById("fileName").innerHTML = data.filenames
              .map((file, index) => `<div>${file} </div>`)
              .join("");
          } else {
            console.error("Upload failed:", response.statusText);
            alert("Upload failed. Please try again.");
          }
        } catch (error) {
          console.error("Error during upload:", error);
          alert("Upload failed. Please try again.");
        }
      }

      // Function to update navigation links after the upload
      function updateNavLinks(hashes) {
        let links = [
          { base: "http://0.0.0.0:80/upload", id: "uploadLink" },
          { base: "http://0.0.0.0:80/frequency", id: "frequencyLink" },
          { base: "http://0.0.0.0:80/length", id: "lengthLink" },
        ];

        links.forEach((link) => {
          if (link.base && link.id) {
            let url = link.base.includes("?")
              ? `${link.base}&hashes=${hashes}`
              : `${link.base}?hashes=${hashes}`;
            const linkElement = document.getElementById(link.id);
            if (linkElement) {
              linkElement.href = url;
            } else {
              console.warn(`Element with id ${link.id} not found.`);
            }
          } else {
            console.error("Invalid link object:", link);
          }
        });
      }
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>

    <!-- Your Custom JS File -->
    <script src="static/links.js"></script>
  </body>
</html>
