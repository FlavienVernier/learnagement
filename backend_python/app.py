from fastapi import Depends, FastAPI, Request
import uvicorn
import logging

from system import authenticate, check
from user import LNM_enseignant
from user import LNM_university
from user import APC_competence

access_logger = logging.getLogger("uvicorn.access")

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(authenticate.router)
app.include_router(check.router)
app.include_router(LNM_enseignant.router)
app.include_router(LNM_university.router)
app.include_router(APC_competence.router)

# app.include_router(
#     authenticate.router,
#     prefix="/authenticate",
#     tags=["authenticate"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

# Classical health
@app.get("/health")
def health():
    return {"status": "ok"}

# make health silent (without log)
@app.middleware("http")
async def silence_health_logs(request: Request, call_next):
    if request.url.path == "/health":
        access_logger.disabled = True
        response = await call_next(request)
        access_logger.disabled = False
        return response
    return await call_next(request)
@app.get("/")
async def root():
    return {"message": "Hello, I'm Learnagement BackEnd!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)