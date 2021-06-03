import requests
import pathlib
import os
for sol in os.listdir():
    if sol in ["send.py", "moves"]:
        continue
    os.system(f"python3 {sol}")
    requests.post("http://localhost:8000/simulate",
                  json={"team_name": sol, "code": pathlib.Path("moves").read_text()})
