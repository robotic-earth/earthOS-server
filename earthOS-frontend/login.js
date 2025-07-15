document.getElementById("login").addEventListener("submit", function(event) {
  event.preventDefault(); 
});

const username = document.getElementById("username").value;
const password = document.getElementById("password").value;

fetch("/login",{
    method: "POST",
    headers: {
        "content-type": "application/json"
    },
    body: JSON.stringify({username, password})
})
.then(Response => Response.json())
.then(data => {
    if (data.success) {
        alert("successful login");
    } else {
        alert("something went wrong with the login.");
    }
})
.catch(error => {
    console.error("Error", error)

});
