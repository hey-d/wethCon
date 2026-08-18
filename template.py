import os 
from path import Path

list_of_files = [
    "./app.py",
    "./tools.py"
]

for file in list_of_files:
    path = Path(file)
    
    filedir = path.parent
    
    if filedir != "":
        os.makedirs(filedir, exist_ok =True)
        
    if not path.exists():
        with open (path, "w") as f:
            pass