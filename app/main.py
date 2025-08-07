from fastapi import FastAPI

from routes import router


app = FastAPI(title="Shay Zilberman's Home Assigment")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
