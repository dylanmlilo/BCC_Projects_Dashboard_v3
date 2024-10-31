function validateProfilePassword() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password) {
        if (password.length < 8 || password.length > 20) {
            alert("Password must be between 8 and 20 characters long.");
            return false;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match. Please try again. If you are not updating the password please leave it blank.");
            return false;
        }
    }

    return true; 
}