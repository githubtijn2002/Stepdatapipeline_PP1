
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PORT = 8080
EXPOSE 8080

CMD ["python", "mock_api.py"]