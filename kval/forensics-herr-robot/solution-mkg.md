# Herr Robot

Vi får en mystisk fil, `BA424D26411F9430EE5EB653314484FFBE8DCEDD`. Med hjälp av programmet `file` i linux kan vi ta reda på vad det är för fil:

```sh
$ file BA424D26411F9430EE5EB653314484FFBE8DCEDD
BA424D26411F9430EE5EB653314484FFBE8DCEDD: 7-zip archive data, version 0.4
```

Vi kan extrahera arkivet med följande kommando:

```sh
7z e BA424D26411F9430EE5EB653314484FFBE8DCEDD
```

Vi får då fram filen `robot`. Mha. `file` får vi reda på att det är en `jpeg`. Om vi tittar på den ser vi Elliot från Mr. Robot. Det kan vara så att något är gömt i bilden. Det finns flera sätt att undersöka efter gömda saker i bilder, även känt som stegonografi. Man kan dels använda [`Stegsolve.jar`](https://www.aldeid.com/wiki/Stegsolve), ett verktyg för att snabbt kunna upptäcka vanliga stegonografi-tekniker. När vi använder Stegsolve hittar vi dock inget. Man kan då undersöka filen i en bildredigerare lite mer om man vill. Man kan också försöka hitta originalbilden genom "reverse image search" på Google eller med [TinEye](https://tineye.com/).

Men i det här fallet valde jag att istället titta på filens innehåll för att se om det fanns något skumt där. Man kan kolla vilken metadata (EXIF-data) som jpeg-filen innehåller, men hittar då inget av intresse. Det kan vara bra att köra `strings` på filen. Då plockas alla ASCII-strängar i filen ut. I slutet av utdatan från `strings` ser vi massor av `LAME3.100`. Detta verkar intressant då jag aldrig har sett något sånt i en jpg-fil förut. Om man Googlar runt lite på LAME3 ser man att det har något med ljud att göra. Hmmm, ljud i vår bildfil? Detta verkar skumt. Lite högre upp i utdatan från `strings` ser vi:

```
TPE1
TALB
TYER
TCON
TRCK
COMM
Find the flag
Info
```

Suspekt med "Find the flag". Om man Googlar runt på de andra orden får man igen upp referenser till ljud och ljud-filer. Det verkar som att det finns en ljudfil gömd i vår bildfil. Vanligtvis när man vill hitta filer gömda i andra filer kan man använda verktygen `binwalk` eller `foremost`. Men i det här fallet hittar de ingenting när man använder dem. Ett annat verktyg som är väldigt bra för att undersöka filer mer i detalj är [010editor](https://www.sweetscape.com/010editor/). Med hjälp av deras binary templates visas den faktiska strukturen av filerna och man kan undersöka alla värden i alla fält. Öppna `robot` i 010editor och välj "Templates -> Image -> JPG". Då kommer nedre delen av fönstret att visa strukturen hos filen. Längs ner i listan över områden i filen ser vi `char unknownPadding[85179]`. Om vi klickar på den delen i listan så visas den motsvarande binära datan i hexdumpsvyn. Där kan vi se att detta område börjar med de strängar vi hittade nyss. Det här verkar vara där JPG:en tar slut och där något annat börjar. I 010editor kan vi ta bort allt innan denna punkt och bara spara den okända paddingen i en egen fil. Om vi gör detta får vi ett nytt resultat när vi använder `file`:

```sh
$ file robot 
robot: Audio file with ID3 version 2.3.0, contains:MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, Stereo
```

Vi kan försöka spela upp den här filen mha. VLC. Det vi hör är bara konstigt pipande utan någon struktur. När man vill undersöka ljudfiler är [Audacity](https://www.audacityteam.org/) ett väldigt bra verktyg. Där kan man se vågformen och leta efter mönster bland pip. Till exempel för att upptäcka morsekod eller liknande. Audacity är också väldigt bra för att kunna redigera ljudfiler, applicera filter, osv. osv. Den vanliga vyn visar vågformen baserat på volymen som spelas upp. När vi öppnar filen ser vi inget intressant där, volymen går upp och ner utan något tydligt mönster. Ett annat vanligt knep är att gömma saker i ett spektrogram. Om man visar ett spektrogram för en ljudfil så visas vilka frekvenser som spelas vid en viss tidspunkt. Jag vet inte hur jag ska beskriva hur man väljer att visa spektrogram istället för vanlig vågform, så här får du en video där de beskriver hur man ändrar inställningen: https://www.youtube.com/watch?v=VZbZa99ocPU

När vi visar ljudet som ett spektrogram så hittar vi äntligen flaggan!
