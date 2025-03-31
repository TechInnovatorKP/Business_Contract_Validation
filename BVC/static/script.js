function showSignIn() {
    document.getElementById("authPage").style.display = "none";
    document.getElementById("signInPage").style.display = "block";
}

function showSignUp() {
    document.getElementById("authPage").style.display = "none";
    document.getElementById("signUpPage").style.display = "block";
}

function goToAuthPage() {
    document.getElementById("signInPage").style.display = "none";
    document.getElementById("signUpPage").style.display = "none";
    document.getElementById("authPage").style.display = "block";
}

function validateSignIn() {
    document.getElementById("authPage").style.display = "none";
    document.getElementById("signInPage").style.display = "none";
    document.getElementById("uploadPage").style.display = "block";
}

function validateSignUp() {
    document.getElementById("authPage").style.display = "none";
    document.getElementById("signUpPage").style.display = "none";
    document.getElementById("uploadPage").style.display = "block";
}

function validateContract() {
    let fileInput = document.getElementById("fileUpload");
    let contractType = document.getElementById("contractType").value;
    if (fileInput.files.length === 0) {
        alert("Please upload a contract document.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("contractType", contractType);

    fetch("http://127.0.0.1:5000/api/validate-contract", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("uploadPage").style.display = "none";
        document.getElementById("resultPage").style.display = "block";
        document.getElementById("validity").innerText = data.validity + "%";
        document.getElementById("similarityPercentage").innerText = data.similarityPercentage + "%";

        let recommendationsList = document.getElementById("recommendations");
        recommendationsList.innerHTML = "";
        data.recommendations.slice(0, 3).forEach(rec => {
            if (rec.trim() !== "") {
                let listItem = document.createElement("li");
                listItem.textContent = rec;
                recommendationsList.appendChild(listItem);
            }
        });
    })
    .catch(error => alert("Error validating contract."));
}

function goBack() {
    document.getElementById("resultPage").style.display = "none";
    document.getElementById("uploadPage").style.display = "block";
}