Run send.py in solve dir to send all test solution.

# Bugs to implement:
- [x] reset speed on pause
- [x] allow jumping when speed = 0
- [x] compute speed + gravity such that speed = 0 when at the top
- [x] set fps such that it is possible to go through floor if u have enough speed
- [x] create button logic that allows it to be pressed at a certain distance such that it can be pressed from other side of wall (add logic to front-end to hide this somehow) 

# Dev:
- [x] Create good map.
- [x] Create buttons and doors
- [x] Allow player to export run
- [x] Create speedrun website to comfirm that run is valid

# Instructions

## API
```
pip install fastapi
pip install uvicorn
uvicorn api:app 
```


# Score
1600  - 200
2300  - 150
3500  - 100
10000 - 50