# Deploying to Vercel

## Overview

This app has been migrated to use **Tesseract.js** for client-side OCR, making it compatible with Vercel's serverless environment without complex server-side dependencies.

## Steps

1.  **Push to GitHub**: Ensure your latest code (including `vercel.json` and updated `requirements.txt`) is on GitHub.
2.  **Import Project in Vercel**:
    -   Go to [vercel.com/new](https://vercel.com/new).
    -   Import your GitHub repository.
3.  **Configure Project**:
    -   **Framework Preset**: Select **Other**.
    -   **Build Command**: `pip install -r requirements.txt` (or leave default if Vercel detects Python).
    -   **Output Directory**: Leave default.
    -   **Environment Variables**: None required for the basic app.
4.  **Deploy**: Click **Deploy**.

## troubleshooting

-   **"404 Not Found"**: If the app doesn't load, check if `vercel.json` is in the root and correctly points to `app.py`.
-   **Dependencies**: Ensure `pytesseract` is NOT in `requirements.txt`.
