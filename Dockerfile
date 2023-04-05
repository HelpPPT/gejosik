# Get the Fast API image with Python version 3.10
FROM python:3.10

# Create the directory for the container
WORKDIR /
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Konlpy jdk 추가
RUN apt-get update && \
    apt-get install -y default-jdk

# Copy the serialized model and the vectors
COPY ./ ./

# Run by specifying the host and port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]