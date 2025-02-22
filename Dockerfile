FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including awscli and wget
RUN apt-get update && apt-get install -y awscli wget && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variable for the port (Render maps this port)
ENV PORT=8000

# Set environment variables for model location using your S3 URI
ENV MODEL_S3_URI="s3://verifiedx-models-bucket/optimum/"
ENV MODEL_PATH="/app/models/optimum/"

# Re-add PYTHONPATH so that the "/app/src" directory is on the import path
ENV PYTHONPATH="/app/src"

# Create a directory for your model files
RUN mkdir -p ${MODEL_PATH}

# Expose the necessary port
EXPOSE 8000

# At startup, download the model folder in the background and then run the FastAPI app.
CMD aws s3 cp ${MODEL_S3_URI} ${MODEL_PATH} --recursive & uvicorn api.routes:app --host 0.0.0.0 --port 8000