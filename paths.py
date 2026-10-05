# =================================================
# Defines all the folder paths used for the project 
# =================================================

from pathlib import Path

PROJECT_NAME = "DATA422_group_project"

def project_root():
    # Start at this file and walk up until we find the project folder
    p = Path(__file__).resolve()
    while p.name != PROJECT_NAME:
        p = p.parent
    return p

def data_path(*parts):
    return project_root() / "Data" / Path(*parts)

def code_path(*parts):
    return project_root() / "Code" / Path(*parts)

def out_path(*parts):
    return project_root() / "out" / Path(*parts)