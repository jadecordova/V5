// Call Python's greet function from JavaScript
function callGreet() {
    const name = document.getElementById('nameInput').value || 'World';
    const resultDiv = document.getElementById('greetResult');

    // Call the Python function exposed with @eel.expose decorator
    eel.greet(name)(function (result) {
        resultDiv.textContent = result;
        resultDiv.classList.add('show', 'success');
    });
}

// Get Python data
function getPythonData() {
    const infoDiv = document.getElementById('pythonInfo');

    eel.get_python_info()(function (data) {
        infoDiv.innerHTML = `
            <strong>${data.message}</strong>
            <pre>${data.python_version}</pre>
        `;
        infoDiv.classList.add('show');
    });
}

// Allow Enter key to trigger greeting
document.addEventListener('DOMContentLoaded', function () {
    const nameInput = document.getElementById('nameInput');
    nameInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            callGreet();
        }
    });
});
