"""Entry point — starts the FastAPI service and all agent loops."""
import uvicorn
from loops.scheduler import start_all
from service.api import app

if __name__ == "__main__":
    start_all()
    uvicorn.run(app, host="0.0.0.0", port=8080)