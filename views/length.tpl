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
    <script type="text/javascript" src="/static/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.2.2/Chart.min.js"></script>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
      rel="stylesheet"
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
            class="nav-link"
            href="frequency?order=frequency"
            id="frequencyLink"
            >Word Frequency</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link active" href="length" id="lengthLink"
            >Word Lengths</a
          >
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
        <div class="row">
          <div class="col">
            <div class="form-check form-switch">
              <input
                class="form-check-input"
                type="checkbox"
                id="toggleSwitch"
              />
              <label class="form-check-label" for="toggleSwitch"
                >Group lengths</label
              >
            </div>
          </div>
        </div>

        <div class="row">
          <canvas id="myChart" style="margin: 10px"></canvas>
        </div>
      </div>
    </div>
  </body>

  <script>
    async function fetchData() {
      const currentUrl = new URL(window.location.href);
      const searchParams = currentUrl.searchParams;

      const response = await fetch(
        "https://webpageparser.onrender.com/length-data?" + searchParams
      );
      const data = await response.json();
      return data;
    }

    async function renderChart() {
      const ctx = document.getElementById("myChart").getContext("2d");
      const chartData = await fetchData();

      new Chart(ctx, {
        type: "bar", // Change type as needed
        data: chartData,
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true, offset: true },

            x: {
              offset: true,
            },
          },

          legend: {
            display: false,
          },
        },
      });
    }

    renderChart();
  </script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // JavaScript to handle the switch toggle and URL manipulation
    const toggleSwitch = document.getElementById("toggleSwitch");

    // Check if the switch state exists in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentState = urlParams.get("grouped");

    if (currentState === "true") {
      toggleSwitch.checked = true;
    }

    toggleSwitch.addEventListener("change", function () {
      // Get current URL
      const currentUrl = new URL(window.location.href);

      // Get current query parameters
      const searchParams = currentUrl.searchParams;

      // Set or update the query parameter for the switch state (e.g., "optionEnabled")
      searchParams.set("grouped", toggleSwitch.checked ? "true" : "false");

      // Update the URL with the new query parameter
      currentUrl.search = searchParams.toString();

      // Redirect to the new URL
      window.location.href = currentUrl.toString();
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
      downloadLink.href = baseDownloadUrl + queryParams + "&page=lengths";
    };
  </script>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

  <script src="static/links.js"></script>
</html>
