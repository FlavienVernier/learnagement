from fastapi import Depends, FastAPI, Request
import uvicorn
import logging

from system import authenticate, check
from user import LNM_enseignant
from user import LNM_university
from user import APC_competence

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

access_logger = logging.getLogger("uvicorn.access")
class HealthFilter(logging.Filter):
    def filter(self, record):
        return "/health" not in record.getMessage()

access_logger.addFilter(HealthFilter())

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
        previous_state = access_logger.disabled
        access_logger.disabled = True
        try:
            response = await call_next(request)
        finally:
            access_logger.disabled = previous_state
        return response
    return await call_next(request)
@app.get("/")
async def root():
    return {"message": "Hello, I'm Learnagement BackEnd!"}

if __name__ == "__main__":
    print(bcolors.OKGREEN + "Start backend Python..." + bcolors.ENDC)
    uvicorn.run(app, host="0.0.0.0", port=4000)