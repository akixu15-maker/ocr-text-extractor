# Deploying to Render.com

## Steps

1.  **Push to GitHub**: Ensure your code (including `Dockerfile` and `requirements.txt`) is pushed to your GitHub repository.
2.  **Create New Web Service**:
    -   Go to [dashboard.render.com](https://dashboard.render.com/).
    -   Click "New +" -> "Web Service".
    -   Connect your GitHub repository.
3.  **Configure Service**:
    -   **Name**: Choose a name (e.g., `streamlit-ocr`).
    -   **Region**: Choose a region (e.g., Oregon or Frankfurt).
    -   **Branch**: `main` (or your working branch).
    -   **Runtime**: **Docker**.
    -   **Build Command**: Leave blank (Docker handles this).
    -   **Start Command**: Leave blank (defined in `CMD` of Dockerfile).
    -   **Plan**: Free.
    -   **Note**: The repository includes a `Dockerfile` specifically optimized for Render, installing Tesseract and all necessary system libraries.

4.  **Advanced (Env Vars)**:
    -   Render automatically sets `PORT`.
    -   We explicitly set `ENV PATH="/usr/bin:$PATH"` in the Dockerfile, so no extra config needed here.
5.  **Deploy**: Click "Create Web Service".

## Troubleshooting

-   **Tesseract Error**: If you see "TesseractNotFoundError", ensure the `Dockerfile` effectively installed `tesseract-ocr` and `app.py` points to `/usr/bin/tesseract`.
-   **Port Error**: If the app doesn't load, check the logs. Streamlit should say "listening on port ...". Render expects the app to bind to `0.0.0.0` and the port in `$PORT`.
