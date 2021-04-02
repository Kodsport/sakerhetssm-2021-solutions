# Undvik Handskakning

När man besöker hemsidan står det hur de har bytt tjänsten till UDP istället för TCP för att undvika handskakningar. Detta betyder att vi måste ansluta mha. UDP till samma IP istället för TCP som HTTP vanligtvis är byggt med. När vi läser sidkällan står det att om man vill ha en hint så ska man leta högre upp. Vad kan det betyda? Vad kommer högre upp än HTML:en på en hemsida? Om man tänker på protokollnivå så kommer statuskoden och samlingen av headers "högre upp" än kroppen (som innehåller HTML:en) i ett HTTP response. Sagt och gjort, vi måste se vad för headers som skickades tillbaka av servern. Ett sätt att göra detta är att använda `curl`:

```sh
curl -i http://sentorchallenge.se/
```

`-i` gör att headerna skrivs ut i terminalen. Där ser vi nu att man kan använda ett verktyg som heter `socat` för att enkelt göra den här "kommunikationen med HTTP, fast över UDP". Efter att han kollat upp hur man använder `socat` kan man komma fram till följande kommando att köra:


```sh
socat TCP-LISTEN:8080,reuseaddr,fork UDP-CONNECT:sentorchallenge.se:80
```

Om man nu besöker http://localhost:8080 i sin webbläsare så kommer man se sidan. Där berättas att de har haft problem med ett visst kommando när det körs i Bash. Om man kopierar kommandot och kör det i sin terminal ser man outputet: 

```
Is that a flag in your /tmp dir?
```

Om man kollar i sin `/tmp`-mapp så ser man filen `flag-ssm2021.txt`. När man tittar i den så ser man:

```
Or are you
just happy
to see me?
```

Ingen flagga där inte. Hmmm. När man kopierar in den andra texten de refererar till på hemsidan så expanderar den till något väldigt långt som innehåller massa saker som ser ut ungefär så här:

```
\033[3C{\033[9Ct\033[6Dr\033[2Ca\
```

För att se vad som händer på den här hemsidan kan man kolla i sidkällan. Där ser man att en hel del text har dolts mha. CSS. Där ser vi att de första kommandot faktiskt bestod av flera kommandon som skrev till filen i /tmp och sedan skrev ut något annat på skärmen än vad man hade trott. Man kan också hitta den dolda texten med de konstiga tecknen ovan.

Om man försöker ta reda på vad dessa tecken betyder så kan man komma att hitta något som heter [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code). Om man läser på wikipedia-sidan om det så hittar man att de kan kontrollera färg av terminaltext, men också vart "pekaren" som bestämmer vart nästa tecken på skärmen skrivs ut är. Man kan läsa på att de konstiga tecknena ovan faktiskt säger "gå fram X steg" och "gå bak X steg". För att nu kunna se den riktiga texten som menas, med alla positionsförflyttningar kan man skriva ett python-skript som rör sig i en sträng och skriver bokstäver på rätt ställen. Eller så kan man bara använda kommandot `echo` för att skriva ut strängen i terminalen. Eftersom terminalen faktiskt tolkar dessa tecken och gör förflyttningen av pekaren. När man gör detta får man flaggan!
