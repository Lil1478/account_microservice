# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose a PORT to access the python application
EXPOSE $PORT

# Run app.py when the container launches
CMD exec uvicorn app:app --host 0.0.0.0 --port 8080