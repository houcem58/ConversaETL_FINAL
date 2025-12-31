# Quick Start

\\\ash
pip install -r requirements.txt
python examples/basic_example.py
python app.py
\\\
"@ | Out-File -FilePath "docs/QUICKSTART.md" -Encoding utf8

# Dockerfile
@"
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
