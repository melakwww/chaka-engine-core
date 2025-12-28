FROM apify/actor-python:3.11

# Copy all files into the container
COPY . ./

# Install requirements
RUN pip install -r requirements.txt

# Start the Python engine
CMD ["python3", "-m", "src.main"]