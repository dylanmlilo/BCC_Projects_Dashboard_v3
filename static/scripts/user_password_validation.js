function validateUserPassword(form) {
    const password = form.password.value;

    if (password === "") {
        return true;
    }

    if (password.length < 8 || password.length > 20) {
        alert("Password must be between 8 and 20 characters long.");
        return false;
    }

    return true;
}