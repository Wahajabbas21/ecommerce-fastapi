from app.main import app as fastapi_app
from mangum import Mangum

app = Mangum(fastapi_app)


