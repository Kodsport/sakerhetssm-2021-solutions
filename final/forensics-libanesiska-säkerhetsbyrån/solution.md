# Libanesiska säkerhetsbyrån

Genom att öppna bilden i något godtyckligt ritprogram kan man direkt märka att de översta pixlarna inte har samma nyans av röd. Detta är då den minsta signifikanta biten (LSB) har modifierats i dessa pixlar. (Även titeln är en hint till LSB). Datan som är gömd kan fås ut genom att använda exempelvis zsteg:

```
zsteg flag.png b1,rgb,lsb,xy -l 1000000
```

Med detta får vi ut brainfuck-kod som kan köras med exempelvis https://copy.sh/brainfuck/ för att få ut en sträng bestående av pi, ka, pipi, pichu, pika, chu, pikachu och pikapi. Detta är en variant av brainfuck där tecknen har bytts ut mot olika läten från pikachu. Vi kan nu slutligen använda https://www.dcode.fr/pikalang-language för att få ut flaggan:

```
SSM{l3g3nd3n_v4r_s4nn_tr0ts_4llt}
```
