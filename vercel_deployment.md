# Deploying to Vercel

## Overview

This app has been migrated to use **Tesseract.js** for client-side OCR. It runs as a Streamlit app on Vercel's Python runtime, but the heavy image processing happens in the user's browser.

## Steps

1.  **Push to GitHub**: Ensure your code is pushed to your GitHub repository.
2.  **Import Project in Vercel**:
    -   Go to [vercel.com/new](https://vercel.com/new).
    -   Import your `streamlit-ocr` repository.
3.  **Configure Project**:
    -   **Framework Preset**: Select **Other**.
    -   **Root Directory**: `.` (default).
    -   **Build Command**: `pip install -r requirements.txt` (or leave empty if Vercel defaults work).
    -   **Output Directory**: `.` (or override to current directory if needed).
    -   **Environment Variables**: None required.
4.  **Deploy**: Click **Deploy**.

## Custom Domain Setup

To add a custom domain (e.g., `ocr.example.com`):
1.  Go to your Project Settings > **Domains**.
2.  Enter your domain name.
3.  Follow the instructions to add the **CNAME** or **A Record** in your DNS provider (e.g., Namecheap, Cloudflare).
    -   CNAME: `cname.vercel-dns.com`
4.  Vercel automatically handles SSL certificates.

## Limitations

> [!WARNING]
> **Streamlit on Serverless**: You might see a "Connection Lost" message occasionally because Streamlit relies on WebSockets, which have timeout limits on Vercel Serverless Functions. However, since the OCR processing happens in the browser via Javascript, the extraction should still work even if the server connection flakiness occurs.
