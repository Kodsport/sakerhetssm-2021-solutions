from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, routing, Body, HTTPException
from pydantic import BaseModel
import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from game.game import GameState
from game.constants import INPUTS, SCANCODE_TO_NAME
import sqlite3
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()
connection = sqlite3.connect("scoreboard.db")


origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# CONST
MAX = 10000
EASY = 3500
HARD = 2300
EXPERT = 1600
IMPOSSIBLE = 1400
EASY_FLAG = "MAX_FLAG"
MEDIUM_FLAG = "MEDIUM_FLAG"
HARD_FLAG = "HARD_FLAG"
EXPERT_FLAG = "EXPERT_FLAG"
IMPOSSIBLE_FLAG = "IMPOSSIBLE_FLAG"


# READ FLAGS


def read_flags():
    global MEDIUM_FLAG, HARD_FLAG, IMPOSSIBLE_FLAG, EASY_FLAG, EXPERT_FLAG
    try:
        EASY_FLAG = Path("flag0.txt").read_text()
        MEDIUM_FLAG = Path("flag1.txt").read_text()
        HARD_FLAG = Path("flag2.txt").read_text()
        EXPERT_FLAG = Path("flag3.txt").read_text()
        IMPOSSIBLE_FLAG = Path("flag4.txt").read_text()
    except:
        print("running with fake flags")


# GAME SIMULATION


def game(code: str):
    game_state = GameState()
    try:
        for ticks, line in enumerate(code.split("\n")):
            game_state.game_loop(int(line))
            if game_state.game_won:
                return ticks + 1
    except ValueError:
        return -1
    return -1


async def run(code):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(app.state.executor, game, code)


# DATABASE


def init_db():
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE scoreboard (team_name TEXT, time INT, run TEXT)")
        cursor.close()
    except:
        pass


def add_time_to_scoreboard(team_name, time, code):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO scoreboard VALUES (?, ?, ?)", (team_name, time, code))
    cursor.close()
    connection.commit()


def get_scoreboard():
    cursor = connection.cursor()
    res = cursor.execute(
        """SELECT team_name, MIN(time) 
        FROM scoreboard 
        GROUP BY team_name
        ORDER BY min(time) ASC;"""
    ).fetchall()
    cursor.close()
    return res


# ENDPOINTS


class Sim(BaseModel):
    code: str
    team_name: str = "Anonymous"


@app.post("/simulate")
async def simulate(payload: Sim):
    l = len(payload.code.split("\n"))
    if l > MAX:
        return HTTPException(status_code=400, detail="code too long")
    if len(payload.team_name) > 30:
        return HTTPException(status_code=400, detail="team name too long")
    res = await run(payload.code)
    if res == -1:
        return {"status": "failed"}
    ret = {"status": "success", "ticks": f"{res}", "flags": [EASY_FLAG]}
    if res < IMPOSSIBLE:
        ret["flags"].append(IMPOSSIBLE_FLAG)
    if res < EXPERT:
        ret["flags"].append(EXPERT_FLAG)
    if res < HARD:
        ret["flags"].append(HARD_FLAG)
    if res < EASY:
        ret["flags"].append(MEDIUM_FLAG)
    add_time_to_scoreboard(payload.team_name, res, payload.code)
    return ret


@app.get("/scoreboard")
async def scoreboard():
    return {"scoreboard": get_scoreboard()}


@app.get("/")
async def index():
    return RedirectResponse("/index.html")


app.mount("/", StaticFiles(directory="/app/web/public"), name="public")

# STARTUP


@app.on_event("startup")
async def on_startup():
    init_db()
    read_flags()
    app.state.executor = ProcessPoolExecutor()


# SHUTDOWN


@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()
    connection.commit()
