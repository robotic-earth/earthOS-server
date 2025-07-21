document.getElementById("login").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Successful login");
        } else {
            alert("Something went wrong with the login.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
