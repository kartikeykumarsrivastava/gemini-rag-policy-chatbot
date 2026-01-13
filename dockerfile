FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask google-genai faiss-cpu pypdf numpy gunicorn

EXPOSE 8000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
