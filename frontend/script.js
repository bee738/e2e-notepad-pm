document.addEventListener('DOMContentLoaded', () => {
    // Placeholder for frontend logic
    console.log("Frontend loaded");

    // **Crucial: Implement End-to-End Encryption in JavaScript here!**
    // 1. Key Generation (WebCrypto API or crypto library)
    // 2. Encryption before sending data to API
    // 3. Decryption after receiving data from API

    // Example API call (replace with actual logic and E2EE)
    async function fetchNotes() {
        const token = localStorage.getItem('accessToken'); // Get token after login
        if (!token) {
            console.log("Not logged in.");
            return;
        }
        try {
            const response = await fetch('/api/notes/', { // Adjust API path if needed
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const notes = await response.json();
            console.log("Notes:", notes);
            // Display notes in UI
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }

    // Example login function (adapt to your login form)
    async function login(username, password) {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        try {
            const response = await fetch('/api/token', { // Adjust API path if needed
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error(`Login failed: ${response.status}`);
            }
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            console.log("Login successful, token:", data.access_token);
            // Redirect or update UI to show logged-in state
            fetchNotes(); // Example: Fetch notes after login
        } catch (error) {
            console.error("Login error:", error);
        }
    }

    // Example registration function (adapt to your register form)
    async function register(username, password) {
        try {
            const response = await fetch('/api/register/', { // Adjust API path if needed
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            });
            if (!response.ok && response.status !== 201) { // Check for 201 Created
                const errorData = await response.json();
                throw new Error(`Registration failed: ${response.status} - ${errorData.detail || 'Unknown error'}`);
            }
            if (response.status === 201) {
                console.log("Registration successful!");
                // Optionally, automatically log the user in or redirect to login page
            }
        } catch (error) {
            console.error("Registration error:", error);
            alert(error.message); // Simple error display for example
        }
    }


    // Example: Call login or register functions from form submissions
    // (You'll need to add form elements in index.html and attach event listeners)
    // ... (Form event listeners and calls to login() or register() functions) ...

});
