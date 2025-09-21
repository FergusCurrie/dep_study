# Dep Study

POC application for solving practice problems. 

FastAPI is used as backend, which generates a problem description in markdown + latex, solution and multi-choice answers. 

React + mui renders the problem for solving. 


## Creating new problem 

1. Define problem name. 
2. Create new template in `problem_templates/<name>.j2`
3. Add python file to `src/problems/<name>.py` with logic for generating question data + solving. 
4. Use `manual_db.py` to add to problem database
5. Update `src/problems/dispatch.py` to correctly dispatch name to problem generation