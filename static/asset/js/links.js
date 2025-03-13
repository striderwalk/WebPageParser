document.addEventListener("DOMContentLoaded", function () {
  // Function to update all navigation links with the current hash
  function updateNavLinks() {
    console.log("The thing...");
    const hash = new URLSearchParams(window.location.search).get("hash"); // Get the hash from the current URL

    // If there's a hash, update the links
    if (hash) {
      const links = [
        { base: "/upload", id: "uploadLink" },
        { base: "/frequency", id: "frequencyLink" },
        { base: "/length", id: "lengthLink" },
      ];

      links.forEach((link) => {
        let url = link.base;
        // Add the hash to the URL
        if (url.includes("?")) {
          url += `&hash=${hash}`;
        } else {
          url += `?hash=${hash}`;
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
