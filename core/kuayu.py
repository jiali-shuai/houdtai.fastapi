
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
import os
import json

load_dotenv(find_dotenv(), override=True)


def setup_cors(app):
    allow_origins = json.loads(os.getenv("CORS_ORIGINS"))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS").lower() == "true",
        allow_methods=json.loads(os.getenv("CORS_ALLOW_METHODS")),
        allow_headers=json.loads(os.getenv("CORS_ALLOW_HEADERS")),
        expose_headers=json.loads(os.getenv("CORS_EXPOSE_HEADERS")),
    )
