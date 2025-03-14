document.addEventListener("DOMContentLoaded", function () {
  // Function to update all navigation links with the current hash
  function updateNavLinks() {
    console.log("The thing...");
    const hashes = new URLSearchParams(window.location.search).get("hashes"); // Get the hash from the current URL

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
