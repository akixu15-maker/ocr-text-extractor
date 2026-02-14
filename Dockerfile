FROM python:3.10-slim-bookworm

# Install system dependencies including Tesseract and its language packs
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-jpn \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Verify Tesseract installation in build logs
RUN tesseract --version

WORKDIR /app

COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly add /usr/bin to PATH (though it should be there by default)
ENV PATH="/usr/bin:$PATH"

# Expose the port (Render sets $PORT env var)
EXPOSE $PORT

# Command to run the app using the PORT environment variable
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
