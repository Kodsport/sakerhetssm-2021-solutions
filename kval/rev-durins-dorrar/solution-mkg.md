# Durins Dörrar

Öppna `speak_friend_and_enter` i ett godtyckligt program för att analysera binärer, så som IDA, Binary Ninja eller Ghidra. Hitta funktionen `main`. Se att kontrollen av lösenordet görs med en enkel `strcmp` mot flaggan. Där ser man vad flaggan är.

## Enklare lösning

Använd linux-verktyget `strings` som visar alla ASCII-strängar i en fil. Följande kommando ger flaggan:

```sh
strings speak_friend_and_enter | grep SSM 
```
