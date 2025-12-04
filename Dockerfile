# Base image
FROM python:3.13-slim

# Sets working directory
WORKDIR /app

# Copies all code
COPY . .

# Install build tools (used ChatGPT)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Runs dependencies
RUN pip install .

# Runs the game
CMD ["python", "-m", "Dinosaur_Venture.dinosaur_venture"]