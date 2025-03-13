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
        <input type="file" id="fileInput" class="d-none" />
      </div>

      <!-- Upload Button -->
      <button class="btn btn-primary w-100 mt-3" id="uploadBtn" disabled>
        Upload
      </button>

      <div id="hashDisplay" class="alert alert-success mt-3 d-none">
        <strong>File Uploaded:</strong> <span id="fileName"></span>
      </div>
    </div>

    <script>
      const dropZone = document.getElementById("dropZone");
      const fileInput = document.getElementById("fileInput");
      const uploadBtn = document.getElementById("uploadBtn");
      let selectedFile = null;

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
          selectedFile = event.dataTransfer.files[0];
          dropZone.innerHTML = `<strong>${selectedFile.name}</strong> selected`;
          uploadBtn.disabled = false;
        }
      });

      // Handle Click to Select File
      dropZone.addEventListener("click", () => {
        fileInput.click();
      });

      fileInput.addEventListener("change", (event) => {
        if (event.target.files.length > 0) {
          selectedFile = event.target.files[0];
          dropZone.innerHTML = `<strong>${selectedFile.name}</strong> selected`;
          uploadBtn.disabled = false;
        }
      });

      // Handle File Upload
      uploadBtn.addEventListener("click", async () => {
        if (!selectedFile) return alert("No file selected!");

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
          // Make the upload request to the correct port (8000)
          const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
          });

          // Check if response was successful
          if (response.ok) {
            const data = await response.json();
            if (data.hash) {
              // Update the hash display
              document.getElementById("fileName").textContent = data.filename;
              document.getElementById("hashDisplay").classList.remove("d-none");

              // Call function to update nav links
              updateNavLinks(data.hash);
            }
          } else {
            console.error("Upload failed:", response.statusText);
            alert("Upload failed. Please try again.");
          }
        } catch (error) {
          console.error("Error during upload:", error);
          alert("Upload failed. Please try again.");
        }
      });

      // Function to update navigation links after the upload
      function updateNavLinks(hash) {
        let links = [
          { base: "http://localhost:8000/upload", id: "uploadLink" },
          { base: "http://localhost:8000/frequency", id: "frequencyLink" },
          { base: "http://localhost:8000/length", id: "lengthLink" },
        ];

        // Update the href of each link with the hash
        links.forEach((link) => {
          // Check if link.base and link.id are defined
          if (link.base && link.id) {
            let url = link.base;

            // Add hash to the URL
            if (url.includes("?")) {
              url += `&hash=${hash}`;
            } else {
              url += `?hash=${hash}`;
            }

            // Update the link's href if the element is found
            console.log(link.id);
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
