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
    .then(response => response.json())
    .then(data => {
        // Check server response and display result
        if (data.success) {
            alert("Successful login");
        } else {
            alert("Something went wrong with the login.");
        }
    })
    // Log any network or parsing errors
    .catch(error => {
        console.error("Error:", error);
    });
});
