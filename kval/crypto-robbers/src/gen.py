import random

text = """Nu drar vi ut på rövarstråt.
Ja, vi ska ut och röva.
Men bara sånt vi kommer åt,
och sånt vi kan behöva.
Nu är det mörkt kring stad och land,
nu sover folk så gott de kan.
Då drar vi väg med
vår säck och vår spann.
Både Kasper och Jesper och Jonatan.

Vi drar till Kamomilla stad,
till bagerier och butiker.
Vi rövar bröd och marmelad
så ingen blir besviken.
Det händer väl att Jonatan
vill ha en polkagris ibland.
Men annars så tar vi
så lite vi kan
både Kasper och Jesper och Jonatan.
Flaggan är KasperochJesperochJonatan

Vi vet så väl vad vi skall ha
och har så goda nerver.
Hos slaktarn tar vi lejonmat
och fläsk och köttkonserver
och oxfilé är gott minsann
och prickig korv gå också an.
Men annars så tar vi
så lite vi kan,
både Kasper och Jesper och Jonatan.

Sen behöver vi också guld
och tar det om vi kan det
och sen när vi tatt säcken full
så drar vi hem till landet
då är vi hungriga minsann
och mat vi lagar åt varann.
Men annars så gör vi
så lite vi kan,
både Kasper och Jesper och Jonatan.
"""

text = text.upper()

alphabet = list("abcdefghijklmnopqrstuvwxyzåäö".upper())
vokaler = "aeiouyåäö".upper()

permutation = list(range(29))
random.shuffle(permutation)

rov = ""
for c in text:
    if c in alphabet and c not in vokaler:
        rov += c+"O"+c
    else:
        rov += c

enc = ""
for c in rov:
    if c in alphabet:
        ci = alphabet.index(c)
        ei = permutation[ci]
        e = alphabet[ei]
        enc += e
    else:
        enc += c

print(enc)