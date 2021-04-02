# Datorer AB

Börja med att öppna `chall.pcapng` i [Wireshark](https://www.wireshark.org/). Där kan vi analysera trafiken som "packet-capture"-filen innehåller.

Ett bra knep är att högerklicka på något paket, sedan klicka "Follow" och sedan "TCP Stream". Då kan man lätt se vilket data som skickades fram och tillbaka, i rött och blått. Detta fungerar bäst för textbaserade protokoll och inte lika bra för binära protokoll.

När vi undersöker det översta paketet i pcap-filen på detta sätt ser vi en terminal-session som utspelar sig. En användare loggar in på en dator, skriver kommandon och får resultatet skickat tillbaka till sig. Om vi tittar i originalfönstret med listan av alla paket kan vi se att "TELNET" nämns som protokoll. Detta är en föregångare till SSH som skickar all data okrypterad över nätverket.

När vi undersöker terminal-sessionen ser vi att någon loggar in på kontot "vd", tittar runt bland mapparna och till slut zippar ihop alla filer till en fil med namnet `x.zip`. Det ser ut som att personen även krypterar zip-filen med lösenordet `VXozpeHCR4oznGoiijDxCRf8LF4Go9Fc`. 

Det verkar inte finnas så mycket mer information i denna TCP-koppling (TCP-stream). För att byta till nästa koppling kan man klicka i det nedre högra hörnet av fönstret som visar textkonversationen där det finns en ruta som visar vilken "Stream" man är på. Alternativt kan man gå tillbaka till fönstret som visar listan av alla paket och använda sig av filtret `tcp.stream eq N` där N är 0, 1, 2, 3, osv.

I TCP-stream 1 verkar samma person (172.21.0.1) koppla upp sig till samma server (172.21.0.2) som i TCP-stream 0, men den här gången med FTP istället för TELNET. FTP kan användas för att föra över filer mellan datorer. Genom att använda "Follow -> TCP Stream" så kan vi se att personen igen loggar in på kontot `vd`. Lite längre ner i konversationen körs `RETR x.zip`. Detta innebär att personen försöker ladda ner filen x.zip som skapades tidigare. Men var skickas själva filen?

Jo, den skickas i TCP-stream 3. Detta för att FTP använder en TCP-stream för att skicka kommandon och andra TCP-streams för att skicka själva datan som resulterar av kommandona. I TCP-stream 2 kan man se resultatet av att personen i TCP-stream 1 körde kommandot `LIST` som listar alla filer i mappen man är i. Och som sagt, i TCP-stream 3 så överförs zip-filen.

Hur får vi ut zip-filen ur Wireshark? Ett sätt är att i "Follow -> TCP Stream" vyn välja "Show and save data as:" som "Raw", sedan klicka "Save as..." och spara filen. När vi försöker extrahera filen så frågar den oss om lösenordet, som tur är så vet vi ju att det är `VXozpeHCR4oznGoiijDxCRf8LF4Go9Fc`. Nu kan vi se vad som snoddes under dataintrånget. Vi hittar flaggan i `produktideer/flagship.jpg`
