from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/logs")
async def redirect_to_logs(response: Response):
    response = RedirectResponse(url="http:localhost//:8000")
    return response