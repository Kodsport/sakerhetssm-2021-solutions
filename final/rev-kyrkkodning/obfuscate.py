from pathlib import Path
import re

source = Path("challeasy.py").read_text()

names = [row.split(" = ")[0] for row in source.split("\n") if " = " in row]

for i,name in enumerate(names):
    source = re.sub("\\b"+name+"\\b",chr(ord("A")+i),source)

Path("challhard.py").write_text(source)
