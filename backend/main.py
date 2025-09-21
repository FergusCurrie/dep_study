
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.bytes2bits import generate_problem
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    #allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Add this line
)


@app.get("/")
def read_root():
    return {"problem": generate_problem()}

