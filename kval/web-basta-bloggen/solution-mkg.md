# Bästa bloggen

När vi tittar runt på bloggen ser vi att vilket blogginlägg som visas beror på GET-parametern `id` i URL:en. Den kan vara värd att undersöka. När vi testar med 0, 1 och 2 ser vi blogginlägg. Men om vi testar högre siffror så visas inget på skärmen. Samma sak om vi skriver in -1 eller mindre. Gissningsvis så sparas blogginläggen i en databas som webbservern pratar med och gissningsvis är det en SQL-databas då dessa är de mest vanliga. En vanlig sårbarhet som är värd att kolla efter är SQL-injection (SQLi). Den uppstår när man lägger in användarkontrollerade strängar direkt i SQL-statements. Detta gör så att användaren kan kontrollera delar av SQL-koden som körs på databasen.

- Du kan läsa mer om SQLi här: https://en.wikipedia.org/wiki/SQL_injection
- Eller kolla på videos om det här: https://www.youtube.com/results?search_query=sql+injection
- Det här är en väldigt bra resurs för vanliga saker man vill göra med SQLi i olika databaser: http://pentestmonkey.net/category/cheat-sheet/sql-injection

Hur kan vi kolla om vi har en SQLi-sårbarhet här? Då måste vi först föreställa oss hur SQL-statementet kan se ut. Det skulle kunna se ut något i stil med det här:

```sql
SELECT ... FROM ... WHERE id = <VÅR_INDATA_HÄR>
```

Om så är fallet skulle vi kunna verifiera det genom att skicka in `id=0 AND 1=2`. Då skulle SQL:en se ut så här:

```sql
SELECT ... FROM ... WHERE id = 0 AND 1=2
```

Då detta alltid är falskt så borde resultatsidan se ut som den gör när vi skickar in en för hög siffra. Och det gör den! Tjoho! Men sidan kanske bara inte visar något när man skickar in strängar som inte är siffror. Så vi behöver testa mer. Tänk om vi skriver in följande `id=5 OR 1=1`. Det skulle se ut så här:

```sql
SELECT ... FROM ... WHERE id = 5 OR 1=1
```

Blogginlägg 5 finns inte, det har vi redan kollat. Så då borde de bli en blank sida. Men med `OR 1=1` så är ju formeln alltid sann. Detta gör att SQL:en kommer att returnera något, gissningsvis det första den hittar, dvs. första blogginlägget. Om vi testar så visar det sig att det stämmer! Tjoho! Nu kan vi vara ganska säkra på att `id`-parametern är sårbar för SQLi. Vi kan göra ett sista test bara för skojs skull, den här gången med `id=1%2B1`. `%2B` är pluss (`+`) fast [URL-enkodat](https://gchq.github.io/CyberChef/#recipe=URL_Encode(true)&input=Kw). När webbservern läser strängen vi skickar den så kommer den att konvertera det tillbaka till `+` innan det läggs in i SQL:en. Varför kan man inte bara skriver `+` direkt? För att det konverteras till ett mellanslag. Då har vi följande SQL:

```sql
SELECT ... FROM ... WHERE id = 1+1
```

När detta evalueras så borde vi se blogginlägg nummer 2, och det gör vi! Nu vidare till att utnyttja SQLi:n.

Vi kommer använda oss av något som kallas `UNION-based SQLi`. Detta betyder att vi slänger på `UNION` på det redan existerande queryt och `SELECT`:ar lite mer saker. Ett vanligt användningsfall för `UNION` kan se ut såhär:

```sql
SELECT id, username FROM users UNION SELECT id, username FROM admins;
```

Här läggs resultaten av de enskilda förfrågningarna på varandra. Viktigt att notera är att båda `SELECT`-delarna måste be om samma antal kolumner från tabellen, annars funkar det inte!

Så för att kunna göra vår `UNION-based SQLi` måste vi ta reda på hur många kolumner som den första `SELECT`:en frågar efter. Detta kan vi göra genom att skicka in `1 ORDER BY n` där n är vår gissning på hur många kolumner som finns. Ettan i början är vårt inläggs-id. Om vi testar detta med 1 och 2 så får vi fram inlägget, men om vi testar med 3 så ser sidan ut som när vi väljer ett för stort id. Vi kan då dra slutsatsen att den första `SELECT`:en använder 2 kolumner.

För att vår union ska funka måste även datatyperna matcha i kolumnerna från de två `SELECT`:arna. Detta kan man lösa med följande metod. Börja först med att `UNION`:a med en select lika många `null` som antalet kolumner. Så här:

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 1 UNION SELECT null, null;
```

Det vi då skickar in som id-parametern är `1 UNION SELECT null, null;`. `null` kan `UNION`:as med alla andra datatyper. Sedan är det bara att börja gissa en efter en vad kolumnerna faktiskt har för datatyp. Vanliga exempel är strängar eller nummer.

```sql
-- Test för nummer:
SELECT kolumn1, kolumn2 FROM ... WHERE id = 1 UNION SELECT 4, null;
-- Test för strängar:
SELECT kolumn1, kolumn2 FROM ... WHERE id = 1 UNION SELECT 'hej', null;
```

Om vi testar båda queryna ovan ser vi att första kolumnen innehåller en sträng, för det var bara med strängversionen som inlägg 1 visades. Genom att göra samma test för andra kolumnen kommer vi fram till att även den är en sträng.

Om vi nu skickar följande kan vi styra vad som visas på hemsidan:

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT 'hej', 'hej';
```

Blogginlägg 5 finns inte, så första `SELECT`en kommer inte att ge något resultat. Om man kombinerar detta med nästa select så visas `hej` och `hej` som titel respektive inläggstext på sidan. Nice! Nu kan vi göra godtyckligt `SELECT` och se resultatet. Dags att börja utforska databasen.

Så vilka tabeller finns i databasen och hur kan vi ta reda på vad de heter? Detta sparas på olika ställen i olika sorters SQL-databaser. Det finns postgresql, mysql, oracle sql, mssql, sqlite3 och säkert ännu fler. Hur kan vi ta reda på vilken vi har att göra med? Vi försöker anropa funktioner som bara existerar i en av dem och ser vad som funkar. Här kommer [pentestmonkeys cheat sheets](http://pentestmonkey.net/category/cheat-sheet/sql-injection) väl till pass.

MySQL är nog den mest populära SQL-databasen. I MySQL finns funktionen `@@version`. Låt oss testa att anropa den!

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT @@version, 'hej';
```

Det funkade inte! Det gjorde att inget visades. Då är det antagligen inte MySQL. Näst på listan att testa är Postgresql som nog är den näst populäraste. Där har vi funktionen `version()` istället.

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT version(), 'hej';
```

När vi testar det får vi följande som svar: `PostgreSQL 12.6 (Ubuntu 12.6-0ubuntu0.20.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0, 64-bit`. Då vet vi att det är PostgreSQL. Jag hittade följande [artikel](https://www.educba.com/postgresql-list-tables/) som berättar att man kan lista alla tabeller i en postgresql-databas genom att titta i den inbyggda tabellen `pg_catalog.pg_tables`. Efter att ha läst artikeln kan vi konstruera följande query:

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT tablename, 'hej' FROM pg_catalog.pg_tables;
```

Men detta query kan vi lista alla tables. Dock bara en i taget. Hur man vi visa nummer två i resultatlistan? Med `LIMIT 1 OFFSET N` kan vi visa den N:te raden i resultatet. N är noll-indexerad.

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT tablename, 'hej' FROM pg_catalog.pg_tables LIMIT 1 OFFSET 0;
```

Dock finns det alldeles för många tabeller att visa, de allra flesta är inbyggda och innehåller inte någon intressant info för oss. Genom att lägga till `WHERE schemaname != 'information_schema' AND schemaname != 'pg_catalog'` filtrerar vi ut de inbyggda tabellerna.

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT tablename, 'hej' FROM pg_catalog.pg_tables WHERE schemaname != 'information_schema' AND schemaname != 'pg_catalog' LIMIT 1 OFFSET 0;
```

Då ser vi att det finns två tabeller kvar: `posts` och `hemlis_jcndsf`. `posts` låter ju som att den innehåller blogginläggen. `hemlis_jcndsf` låter ju dock intressant, vad kan finnas i den? För att kunna `SELECT`a saker från den tabellen måste vi veta vad kolumnerna heter. Detta kan vi hitta i en av de inbyggda tabellerna, precis som vi hittade vilka tabeller som finns. Vi skickar följande:

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT column_name, 'hej' FROM information_schema.columns WHERE table_name = 'hemlis_jcndsf' LIMIT 1 OFFSET 0;
```

Vi får då fram att det finns en kolumn i tabellen med namn `hemlis_laqws`. Vi kan nu äntligen se vad som finns i tabellen!

```sql
SELECT kolumn1, kolumn2 FROM ... WHERE id = 5 UNION SELECT hemlis_laqws, 'hej' FROM hemlis_jcndsf;
```

Och med det sista SQL-statementet får vi äntligen ut flaggan!

## Alternativ lösning

Alternativ lösning som automatiserar allt det här mha. [sqlmap](http://sqlmap.org/) är att bara köra:

```sh
sqlmap -u 'http://localhost:8080/posts?id=0' --dump
```
