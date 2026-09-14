import sys
import os

# Ensure the current directory is in python path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app as fastapi_app
from mangum import Mangum

app = Mangum(fastapi_app)