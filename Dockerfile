# Use the official Python 3.10.9 image as the base image
FROM python:3.10.9

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set the working directory to /app
WORKDIR /app

# Copy the rest of the application code into the container
# COPY . .

# Start the application
# CMD [ "python", "ui.py" ]
CMD [ "streamlit", "run", "ui_alt.py", "--server.port", "8000"]
# CMD [ "python", "hello_world.py" ]
