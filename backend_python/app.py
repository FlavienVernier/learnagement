from fastapi import Depends, FastAPI
import uvicorn

from dependencies import get_query_token, get_token_header
from system import authenticate

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(authenticate.router)
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