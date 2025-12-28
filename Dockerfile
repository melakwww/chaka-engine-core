# Using the official Apify Python base image
FROM apify/actor-python:3.11

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the engine code
COPY . ./

# Run the engine
CMD ["python3", "main.py"]