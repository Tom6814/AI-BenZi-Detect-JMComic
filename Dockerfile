# Stage 1: Build the frontend (Vue 3 + Vite)
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

# Install dependencies and build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup the backend (FastAPI)
FROM python:3.11-slim
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DATA_DIR=/app/data
ENV PYTHONPATH=/app/backend

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose the application port
EXPOSE $PORT

# Start the FastAPI application
WORKDIR /app/backend
CMD ["python", "main.py"]
