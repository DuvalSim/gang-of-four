FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port your app will run on
EXPOSE 8000

ENV ENV "production"

# Command to run your app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
