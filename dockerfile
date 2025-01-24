# Use the official lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8051

# Command to run your Streamlit app
CMD ["streamlit", "run", "sentiment_streamlit.py", "--server.port=8051", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
