import sys
import os

# Add current directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app as fastapi_app
from a2wsgi import ASGIMiddleware

app = ASGIMiddleware(fastapi_app)