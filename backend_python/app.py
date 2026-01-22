from fastapi import Depends, FastAPI
import uvicorn

from system import authenticate, check
from user import LNM_enseignant
from user import LNM_university
from user import APC_competence

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


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)