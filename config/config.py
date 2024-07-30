from dotenv import load_dotenv
import os

load_dotenv()

GRPC_PORT = os.environ.get("GRPC_PORT")
AUTH_SERVICE = os.environ.get("AUTH_SERVICE")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
