# Barad-dur

Vi får en binär som ber om ett lösenord. Målet är att lista ut lösenordet, som kommer att vara samma som flaggan. `strings` ger inget särskilt intressant. Jag använder mig av Ghidra, men det går att använda IDA, Binary Ninja eller vilket annat disassembleringsprogram som helst. Alla adresser är tagna från Ghidra och kan ha ett annat basoffset i andra disassembleringsprogram.

Vi ser att `main`-symbolen är borttagen. För att hitta `main` går vi istället till funktionen `entry` som börjar vid programmets entrypoint. Eftersom programmet är kompilerat med `libc` så anropas `__libc_start_main` med den faktiska `main`-funktionen som första argument. På så sätt tar vi reda på att `main` börjar vid 0x001014f9.

`main` börjar med att anropa `ptrace(PTRACE_TRACEME, 0, 1, 0)`. Systemanropet `ptrace` låter en process ta kontroll över och observera en annan process. Detta används bland annat av debuggers så som `gdb`. Med argumentet `PTRACE_TRACEME` säger man till `ptrace` att låta ens parent-process ta kontroll över en. Parent-processen är alltså den som startade denna process. Efter det kollas i koden om returvärdet är `-1` och i så fall så stängs programmet av. Detta är en vanlig anti-debuggingteknik. Om man startar programmet i `gdb` så kommer `gdb` att först starta själva programmet och sedan `ptrace`:a det. Då `gdb` redan använder `ptrace` på programmet kommer senare anrop till `ptrace` som försöker tracea samma process att returnera -1. Så om vi försöker använda gdb i det här fallet så kommer programmet inte att köra koden vi vill undersöka.

Vi kan lösa det här genom att "patcha" ut de instruktionerna ur binären. När man "patchar" så ändrar man några instruktioner i binären och får en ny binär. Man kan göra det här i Ghidra, IDA, Binary Ninja osv. Men jag brukar göra det direkt i en hex-editor.

Här är assemblyn precis runt anropet till `ptrace`.

```
00101518 b9 00 00        MOV        ECX,0x0
            00 00
0010151d ba 01 00        MOV        EDX,0x1
            00 00
00101522 be 00 00        MOV        ESI,0x0
            00 00
00101527 bf 00 00        MOV        EDI,0x0
            00 00
0010152c b8 00 00        MOV        EAX,0x0
            00 00
00101531 e8 da fb        CALL       ptrace
            ff ff
00101536 48 83 f8 ff     CMP        RAX,-0x1
0010153a 75 16           JNZ        LAB_00101552
```

Vi kan se att efter anropet så jämförs `RAX` som innehåller returvärdet med -1. Om vi bara ersätter assemblyn för anropet till `ptrace`, `e8dafbffff`, med `NOP`s istället (en `NOP` är 0x90) så kommer `RAX` alltid vara 0 när jämförelsen kommer. Så då undviker vi den fällan.

Nu kan vi börja undersöka resten av koden. Koden skriver ut `You fool! No man can kill me!`, läser sedan in användarens indata, modifierar indatan i två olika loopar, anropar en magisk funktion med indatan och anropar tillslut `memcmp` med den modifierade indatan och en konstant byte-array. Om det matchar så skrivs `*stab* https://youtu.be/wmUKSZWVQvo?t=20` ut och vi verkar ha gissat rätt. Så målet är att indatan ska bli samma som den konstanta byte-arrayen. Så vi försöker gå baklänges från den konstanta byte-arrayen tillbaka till inputet.

Det är dags att ta en närmre titt på den magiska funktionen vid 0x00101459 för att se vad den gör med vår indata. Den anropar i sin tur två andra funktioner 0x0010123d och 0x00101311. Den första av dem, 0x0010123d verkar bara ta argument som är konstanta och inte beror på vår indata. Så därför kan vi ignorera vad exakt den funktionen gör. Vi gräver istället djupare in i 0x00101311. 

I 0x00101311 hittar vi ett till anrop till `ptrace` och en loop som loopar över hela längden på indatan, beräknar ett värde och sedan xor:ar indatan med det, byte för byte. Det här är första och ända stället vi har sett indatan modifieras sedan vi lämnade `main`. Det betyder att vi kan tänka hela den magiska funktionen vid adress 0x00101459 som en enda loop som xor:ar indatan med en förbestämd array av bytes. Om vi kör programmet i `gdb`, sätter en breakpoint precis där xor:en utförs och läser vad indatan xor:as med kan vi extrahera xor-streamen. Om vi gör det kan vi sedan reversera hela den magiska funktionens påverkan på indata. 

Men det extra anropet till `ptrace` då? Det är lite klurigt. Om `ptrace` returnerar 0 så sätts två variabler i funktionen till 1 och annars till 0. Man kan tro, vilket jag först gjorde, att detta är ännu ett sätt att hindra oss från att använda `gdb`. Då vill vi ju att `ptrace` ska returnera 0 som den gör vid korrekta anrop. Men om man tänker på hur binären skulle fungera om vi inte hade patchat den så kommer vi fram till ett annat svar. Om binären körs helt vanligt så görs första anropet till `ptrace` i main, anropet lyckas, returnerar 0 och allt är frid och fröjd. Vad händer då när vi kommer till det andra anropet till `ptrace`? Då har redan första anropet gjort så att processens parent har tagit kontroll över programmet och därför borde `ptrace` misslyckas och returnera -1. Så, när binären "körs som den var avsedd att göra" så borde andra `ptrace` returnera -1 och variablerna i funktionen bör sättas till 0.

Men nu vill vi ju köra programmet i `gdb` och plocka ut xor-streamen varje byte för sig. Kommer allt funka som det ska då? Vi har redan patchat bort så första anropet till ptrace aldrig sker, men istället gör ju `gdb` ett ptrace-anrop när binären debuggas, så det jämnar ut sig och det andra anropet till ptrace inuti binären borde returnera -1. Om man vill vara helt säker på att det blir rätt kan man patcha bort det andra anropet till ptrace och se till att variablerna i funktionen sätts till 0.

När vi försöker debugga programmet i `gdb` kan vi stöta på lite problem då programmet har PIE. (Vi kan upptäcka det här mha. verktyget `checksec` som är del av [pwntools](https://github.com/Gallopsled/pwntools).) PIE gör så att kodens adresser ändras mellan varje körning. Detta gör att om vi tar en adress från Ghidra och försker sätta en breakpoint där så kommer det misslyckas för så fort binären startar så är alla adresser annorlunda. Men hur ska vi då göra för att sätta breakpoints? För att kunna göra det på ett smidigt sätt är det bra att skaffa [pwndbg](https://github.com/pwndbg/pwndbg), ett tillägg till gdb som gör många saker mycket lättare. Med det installerat kan vi skriva `start` för att starta programmet och breaka direkt på första instruktionen. Detta händer dock efter binären har flyttat till de riktiga adresserna den kommer att exekvera med. Om vi nu till exempel vill sätta en breakpoint vid den här adressen `0x00101459` som vi har tagit från Ghidra så kan vi använda den nu tillgängliga `$rebase()` funktionen som pwndbg har fixat åt oss för att få PIE-anpassade adresser. Vi kan då skriva såhär: `b *$rebase(0x1459)`.

Om vi nu plockar ut målsträngen som vår modifierade indata jämförs med i main och plockar ut xor-streamen så är vi redo att skriva ett lösningsskript. Vi börjar med att ta målsträngen, xor:a den tillbaka med streamen som vi plockat ut. Sen måste vi reversera de två första looparna i main som modifierar indatan. Båda är relativt simpla, den andra gör lite xor och den första byter plats på de minsta 4 bitarna och de högsta 4 bitarna i varje byte.

Efter att ha skrivit lite python, debuggat varför det blir fel ett tag så har vi ett komplett lösningsskript och får ut flaggan! :) Se solve-mkg.py för det kompletta skriptet.
