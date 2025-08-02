// Handles the login form submission and sends credentials to the server

// Listen for form submission and prevent default behavior
document.getElementById("login").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send a POST request with the entered username and password
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.redirected) {
            // If backend redirects, manually navigate there
            window.location.href = response.url;
        } else {
            alert("Something went wrong with the login.");
        }
    })
    // Log any network or parsing errors
    .catch(error => {
        console.error("Error:", error);
    });
});


  // Wait until the page is fully loaded, then update the login form title based on whether an admin exists.
      window.addEventListener("DOMContentLoaded", function() {
        const title = document.getElementById("form-title");
        fetch("/api/admin-exists")
          .then((response) => response.json())
          .then((data) => {
            if (data.exists === false) {
              title.textContent = "create admin account";
            } else {
              title.textContent = "Login";
            }
          })
          .catch((error) => {
            console.error("Error checking admin:", error);
            title.textContent = "Login";
          });
      });