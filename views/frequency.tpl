<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Bottle web project template" />
    <meta name="author" content="datamate" />
    <link rel="icon" href="/static/favicon.ico" />
    <title>Project</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    <script type="text/javascript" src="/static/jquery.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css"
    />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css"
    />
  </head>
  <body>
    <nav class="navbar navbar-default navbar-static-top">
      <ul
        class="nav nav-tabs flex-column flex-sm-row nav-fill"
        style="width: 100%"
      >
        <li class="nav-item">
          <a class="nav-link" aria-current="page" href="upload" id="uploadLink"
            >Upload</a
          >
        </li>
        <li class="nav-item">
          <a
            class="nav-link active"
            href="frequency?order=frequency"
            id="frequencyLink"
            >Word Frequency</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link" href="length" id="lengthLink">Word Lengths</a>
        </li>
        <vr />

        <li class="nav-item justify-content: flex-end;">
          <a id="downloadLink" class="btn nav-link" href="#">
            <i class="bi bi-download"></i> Download
          </a>
        </li>
      </ul>
    </nav>

    <div class="container mt-5">
      <div class="card shadow p-4">
        <!-- <div class="row">
          <div class="col">
            <a id="downloadLink" class="btn btn-primary" href="#">
              <i class="bi bi-download"></i> Download
            </a>
          </div>
          <div class="col">
            <div class="dropdown">
              <button
                class="btn btn-primary dropdown-toggle"
                type="button"
                id="dropdownMenuButton"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Sorting Options
              </button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li>
                  <a class="dropdown-item" href="#" data-value="frequency"
                    >Frequency</a
                  >
                </li>
                <li>
                  <a
                    class="dropdown-item"
                    href="#"
                    data-value="reverse-frequency"
                    >Reverse Frequency</a
                  >
                </li>
                <li>
                  <a class="dropdown-item" href="#" data-value="alphabetical"
                    >Alphabetical</a
                  >
                </li>
                <li>
                  <a
                    class="dropdown-item"
                    href="#"
                    data-value="reverse-alphabetical"
                    >Reverse Alphabetical</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div> -->

        <div class="row">
          <table id="myTable" class="table table-striped">
            <thead>
              <tr>
                <th>Word</th>
                <th>Frequency</th>
                <th>Length</th>
              </tr>
            </thead>
            <tbody>
              % for item,frequency in zip(data["words"],data["frequency"]):

              <tr>
                <td>{{ item }}</td>
                <td>{{ frequency }}</td>
                <td>{{ len(item) }}</td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
        <div class="row">
          <hr />
        </div>
      </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
      // JavaScript to handle the dropdown selection and URL manipulation
      document.querySelectorAll(".dropdown-item").forEach((item) => {
        item.addEventListener("click", function (event) {
          event.preventDefault();

          // Get the selected option value
          const selectedValue = item.getAttribute("data-value");

          // Get current URL
          const currentUrl = new URL(window.location.href);

          // Get current query parameters
          const searchParams = currentUrl.searchParams;
          console.log(searchParams, currentUrl);

          // Set or update the query parameter (e.g., "option")
          searchParams.set("sort_order", selectedValue);
          console.log(searchParams, currentUrl);

          // Update the URL with the new query parameter
          currentUrl.search = searchParams.toString();

          // Redirect to the new URL
          window.location.href = currentUrl.toString();
        });
      });
    </script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>

    <script>
      $(document).ready(function () {
        $("#myTable").DataTable({
          paging: true,
          lengthMenu: [20, 30, 40, 50],
          searching: true,

          ordering: true,
        });
      });
    </script>
    <script>
      // JavaScript to dynamically append query parameters to the download link
      window.onload = function () {
        // Get the current URL's query parameters
        const currentUrl = new URL(window.location.href);
        const queryParams = currentUrl.search; // This gets the query string (e.g., ?param1=value1&param2=value2)

        // Construct the download link with the query parameters
        const downloadLink = document.getElementById("downloadLink");
        const baseDownloadUrl = "https://webpageparser.onrender.com/download"; // Adjust to your server's download URL

        // Append the query parameters to the download URL
        downloadLink.href = baseDownloadUrl + queryParams + "&page=frequency";
      };
    </script>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        // Function to update all navigation links with the current hash
        function updateNavLinks() {
          console.log("The thing...");
          const hash = new URLSearchParams(window.location.search).get(
            "hashes"
          ); // Get the hash from the current URL

          // If there's a hash, update the links
          if (hashes) {
            const links = [
              { base: "/upload", id: "uploadLink" },
              { base: "/frequency", id: "frequencyLink" },
              { base: "/length", id: "lengthLink" },
            ];

            links.forEach((link) => {
              let url = link.base;
              // Add the hash to the URL
              if (url.includes("?")) {
                url += `&hashes=${hashes}`;
              } else {
                url += `?hashes=${hashes}`;
              }

              // Update the link's href if the element is found
              const linkElement = document.getElementById(link.id);
              if (linkElement) {
                linkElement.href = url;
              }
            });
          }
        }

        // Update the navigation links when the page loads
        updateNavLinks();

        // Listen for popstate to update the links when the user navigates using the browser's back/forward buttons
        window.addEventListener("popstate", updateNavLinks);
      });
    </script>
  </body>
</html>
