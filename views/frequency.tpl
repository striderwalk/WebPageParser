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
  </head>
  <body>
    <nav class="navbar navbar-default navbar-static-top">
      <ul class="nav nav-tabs">
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
      </ul>
    </nav>

    <div class="container">
      <!-- Dropdown styled with Bootstrap -->
      <div class="container mt-5">
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
              <a class="dropdown-item" href="#" data-value="reverse-frequency"
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

      <table class="table">
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

      <div class="row">
        <hr />
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
    <!-- Your Custom JS File -->
    <script src="static/links.js"></script>
  </body>
</html>
