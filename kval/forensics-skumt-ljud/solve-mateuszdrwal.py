import scipy.io.wavfile
import numpy as np

arr = scipy.io.wavfile.read("ljud.wav")[1]

arr = abs(arr)

average_width = 200


arr = np.convolve(arr, np.ones(average_width * 2 + 1), "valid") / (
    average_width * 2 + 1
)  # moving average

arr = arr > max(arr) / 2


arr = arr[np.argmax(arr) :]  # cut to first rising
l1 = len(arr)
arr = arr[np.argmin(arr) :]  # cut to first falling
arr = arr[np.argmax(arr) :]
arr = arr[np.argmin(arr) :]
arr = arr[np.argmax(arr) :]
arr = arr[np.argmin(arr) :]
arr = arr[np.argmax(arr) :]
arr = arr[np.argmin(arr) :]  # cut to falling edge of last sync signal

clock = round((l1 - len(arr)) / 28)

string = ""
while arr.shape != (0,):
    nextmax = np.argmax(arr)
    if not nextmax:
        nextmax = len(arr)
    arr = arr[nextmax:]
    string += "0" * round(nextmax / clock)

    if arr.shape == (0,):
        break

    nextmin = np.argmin(arr)
    if not nextmin:
        nextmin = len(arr)
    arr = arr[nextmin:]
    string += "1" * round(nextmin / clock)

string = string[
    4:
]  # cut first 4 bits because they are part of the last low of the sync signal

string = string[: len(string) // 8 * 8]
print(int(string, 2).to_bytes(len(string) // 8, byteorder="big"))
