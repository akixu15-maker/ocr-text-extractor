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
4.  **Advanced (Env Vars)**:
    -   Render automatically sets `PORT`, which our Dockerfile uses.
    -   No other env vars are strictly required unless you added API keys.
5.  **Deploy**: Click "Create Web Service".

## Troubleshooting

-   **Tesseract Error**: If you see "TesseractNotFoundError", ensure the `Dockerfile` effectively installed `tesseract-ocr` and `app.py` points to `/usr/bin/tesseract`.
-   **Port Error**: If the app doesn't load, check the logs. Streamlit should say "listening on port ...". Render expects the app to bind to `0.0.0.0` and the port in `$PORT`.
