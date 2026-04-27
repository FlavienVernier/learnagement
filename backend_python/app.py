from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

import init

from system import authenticate, check
from user import LNM_enseignant, LNM_etudiant, LNM_evaluation, LNM_filiere,LNM_calendar, LNM_university, MAQUETTE_module

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
origins = [
    "*"
]
app = FastAPI()

# Ajouter le middleware à l'application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Autorise ton port 40080
    allow_credentials=True,
    allow_methods=["*"],              # Autorise GET, POST, OPTIONS, etc.
    allow_headers=["*"],              # Autorise Authorization, Content-Type, etc.
)

app.include_router(authenticate.router)
app.include_router(check.router)
app.include_router(LNM_enseignant.router)
app.include_router(LNM_etudiant.router)
app.include_router(LNM_university.router)
app.include_router(LNM_filiere.router)
app.include_router(MAQUETTE_module.router)
app.include_router(LNM_evaluation.router)
app.include_router(LNM_calendar.router)

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
    print(bcolors.OKGREEN + "Init BD framework..." + bcolors.ENDC)
    init.init()
    print(bcolors.OKGREEN + "Start backend Python..." + bcolors.ENDC)
    uvicorn.run(app, host="0.0.0.0", port=4000)