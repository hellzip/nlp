# Backend setup
FROM python:3.9-slim as backend

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["python", "app.py"]

# Frontend setup
FROM node:16 as frontend

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ .

CMD ["npm", "run", "dev"]
