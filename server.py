import uvicorn
from main import app

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", log_level="info", port=8000)
