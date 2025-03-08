# E2E Encrypted Notepad and Password Manager

This project is a basic structure for an end-to-end encrypted online notepad and password manager.

## Getting Started (Development)

1. **Install Docker and Docker Compose.**
2. **Clone this repository.**
3. **Navigate to the project root directory in your terminal.**
4. **Run `docker-compose up --build` to start the application.**
5. **Backend API will be accessible at `http://localhost:8000`**
6. **Frontend will be accessible at `http://localhost:8081`**

## Production Deployment (Important Considerations)

- **HTTPS:** You MUST set up HTTPS for production. Use a reverse proxy like Nginx or Traefik in Docker to handle SSL termination and route traffic to your backend and frontend containers.
- **Domain Configuration:** Configure your DNS for `randomsubdomain.gizmotrends.blog` to point to your server's IP address.
- **Reverse Proxy for Ports 80 & 443:** Since ports 80 and 443 are in use, you'll need to configure a reverse proxy (e.g., Nginx running on the host or in a separate Docker container) to:
    - Listen on ports 80 and 443 of your host server.
    - Handle SSL termination (Let's Encrypt).
    - Proxy requests to your frontend (e.g., on port 8081 or its internal Docker port) for static content.
    - Proxy API requests (e.g., to your backend on port 8000 or its internal Docker port) to the backend container.
- **Environment Variables and Secrets:**
    - **DATABASE_URL:**  Securely configure your PostgreSQL connection string in production. Consider using Docker Secrets or environment variables managed by your hosting provider.
    - **SECRET_KEY:**  **Generate a strong and truly random SECRET_KEY for JWT in production.** Do NOT use the example "your-secret-key..." value. Store this securely (Docker Secrets, environment variables from a secure configuration management system).
- **Database Security:** Secure your PostgreSQL database in production. Use strong passwords, configure firewall rules, and consider using SSL for database connections if connecting from outside the Docker network (though within Docker Compose network it's often considered secure enough).
- **Backup:** Implement a backup strategy for your database.
- **Monitoring and Logging:** Set up monitoring and logging for your application and server.
- **End-to-End Encryption (Frontend Implementation):** The *most critical* step for production. Implement robust client-side end-to-end encryption in `frontend/script.js`. Use WebCrypto API or a trusted JavaScript crypto library. **This backend code *does not* handle encryption itself; it expects encrypted data from the frontend.**

## API Subdomain (Optional - Not strictly needed for this setup)

For this basic setup, having the API under `/api` on the same domain `randomsubdomain.gizmotrends.blog/api/` is sufficient and simpler.

If you later decide to use a separate subdomain for the API (e.g., `api.randomsubdomain.gizmotrends.blog`), you would:

1. **Configure DNS:** Create a new DNS A record for `api.randomsubdomain.gizmotrends.blog` pointing to your server's IP.
2. **Reverse Proxy Configuration (Nginx example):** In your Nginx configuration, you would have separate server blocks:
    - One for `randomsubdomain.gizmotrends.blog` (serving the frontend).
    - Another for `api.randomsubdomain.gizmotrends.blog` (proxying to the backend API container).
3. **CORS (Potentially):** If your frontend and API are on different domains, you might need to configure CORS headers in your backend to allow requests from the frontend domain. However, serving both from the same base domain is simpler and avoids CORS issues.

## End-to-End Encryption (Important - Frontend Responsibility)

**This backend provides the API for storing and retrieving *encrypted* data.**  The critical part is implementing the end-to-end encryption logic in the `frontend/script.js` (or a more robust frontend framework like React/Vue).

**Key steps for frontend E2EE:**

1. **Key Generation:** Generate strong encryption keys client-side (using WebCrypto API or a library).
2. **Encryption:** Before sending note content or password data to the API to be saved, encrypt it client-side using the generated keys.
3. **Decryption:** When retrieving notes or passwords from the API, decrypt them client-side using the corresponding keys.
4. **Key Management and Storage:** Securely manage and store encryption keys client-side (consider password-based key derivation or browser storage with encryption). **Do not send unencrypted keys to the backend!**

**Remember to replace placeholders (like `your-secret-key-for-jwt-replace-in-production`) with secure values and implement proper HTTPS and other production security measures.**
