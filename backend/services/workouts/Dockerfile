FROM python:3.13
LABEL authors="george"

# Set working directory
WORKDIR /usr/src/workouts

# Copy requirements.txt first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application source code
COPY . .

# Expose a port
EXPOSE 8000

# Command that starts the app
CMD ["fastapi", "dev", "main.py"]