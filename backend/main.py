
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    #allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Add this line
)

practiceProblems = [
  {
    'id': 1,
    'question': "Solve for x: 2x + 5 = 13",
    'options': ["x = 4", "x = 6", "x = 8", "x = 9"],
    'correct': 0,
    'category': "Algebra"
  },
  {
    'id': 2,
    'question': "What is the area of a circle with radius 3?",
    'options': ["6π", "9π", "12π", "18π"],
    'correct': 1,
    'category': "Geometry"
  },
]

@app.get("/")
def read_root():
    return {"problem": practiceProblems[0]}

