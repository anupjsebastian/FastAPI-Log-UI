# Use the official Python 3.10.9 image as the base image
FROM python:3.10.9

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create the logs directory
RUN mkdir /logs

# Set the working directory to /app
WORKDIR /app

# Copy the rest of the application code into the container
COPY . .

# Start the application
# CMD [ "python", "ui.py" ]
# CMD [ "streamlit", "run", "ui_alt.py", "--server.port", "8000"]
# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
# CMD [ "python", "hello_world.py" ]
# CMD ["/usr/bin/supervisord"]
CMD ["/usr/bin/supervisord", "-n"]
