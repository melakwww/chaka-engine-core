# Use the official Apify Python base image
FROM apify/actor-python:3.11

# Install dependencies with correct permissions
COPY --chown=myuser:myuser requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY --chown=myuser:myuser . ./

# Explicitly start the Python engine
CMD ["python3", "-m", "src.main"]