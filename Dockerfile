# Use the official Apify Python base image
FROM apify/actor-python:3.11

# Copy everything into the container
COPY . ./

# Install your dependencies
RUN pip install -r requirements.txt

# Start your engine as a module
CMD ["python3", "-m", "src.main"]