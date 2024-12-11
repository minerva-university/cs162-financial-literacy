# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy backend files and install Python dependencies
COPY ./backend /app/backend
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs


# Set environment variables for the React build
ARG REACT_APP_backend_api
ENV REACT_APP_backend_api=${REACT_APP_backend_api}

# Copy frontend files and build React app
COPY ./frontend /app/frontend
RUN cd /app/frontend && npm install --force && npm run build

# Expose ports for backend and frontend
EXPOSE 5000 443

# Run backend and serve React app
CMD gunicorn --chdir /app backend:app --bind 0.0.0.0:5000 & \
    npx serve -s /app/frontend/build -l 443
