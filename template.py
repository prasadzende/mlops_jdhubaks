import os


dirs=[
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    "notebooks",
    "src"
]

for dir in dirs:
    os.makedirs(dir,exist_ok=True)
    with open(os.path.join(dir,".gitkeep"),"w") as f:
        pass

file_ =[
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    ".gitignore",
    os.path.join("src","__init__.py")
]

for file in file_:
    with open(file,"w") as f:
        pass