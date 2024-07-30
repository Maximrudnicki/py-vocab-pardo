FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I proto --python_out=. --pyi_out=. --grpc_python_out=. proto/*.proto

EXPOSE 50052

CMD ["python", "main.py"]