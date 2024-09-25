# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r server/requirements.txt

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Build the Next.js app
RUN npm run build

# Set the working directory back to /app
WORKDIR /app

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the FastAPI server and Next.js app when the container launches
CMD ["sh", "-c", "cd server && uvicorn main:app --host 0.0.0.0 --port 8000 & cd ../frontend && npm start"]