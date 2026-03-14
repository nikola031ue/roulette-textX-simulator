# Rulet DSL textX

Rulet DSL je domain-specific jezik napravljen pomoću textX alata koji
omogućava korisnicima da opisuju i simuliraju strategije igranja ruleta 
na jednostavan način.

Umesto pisanja python koda ili ručnog praćenja rezultata, korisnik bi mogao da napiše kratku skriptu koja bi opisivala tok igre kao na primer početni budžet, tipove opklada, pravila i strategije.

Pomoću ovog jezika bi se napravila jasna simulacija ruleta koja je laka za eksperimentisanje. Ovim bi se izbeglo pisanje programskog koda, ručno praćenje rezultata kao i komplikacija sa logikom za ponavljanje. 
Rulet DSL bi omogućio opis strategije u nekoliko linija, ponavljanja, statistike i slično.

Krajnji korisnici ovog jezika bi bili igrači koji žele da testiraju svoje strategije i prate analitiku uspešnosti istih bez kucanja koda, excel tabela i ručnih analiza.

# Sintaksa
Primer osnovne sintakse
```
bankroll 500
bet red 20
spin

show_balance
cash_out
```

## Komande
Komande koje korisnik može da zadaje su vezane za upravljanje novcem (bankroll, cach_out), opklade (bet red 20, bet number 7 5, bet even 20...), tok igre (spin, repeat broj_ponavljanja {...}), kontrola rizika (stop_on_win/loss int), logika za automatizaciju (if_win/lose {...}, double_bet) i informacije (show_stats, show_history).

## Martigale strategija
Ova strategija podrazmeva povećavanje uloga posle promašaja kako bi nadoknadila prethodne gubitke.
```
bankroll 500 
repeat 15 { 
    bet black 10 
    spin 
    if_lose { 
        double_bet
    } 
    if_win { 
        reset_bet 
    }
} 
cash_out
```

# Validacija i Vizualizacija Gramatike

## Provera ispravnosti textX gramatike
Da biste proverili da li je `grammar.tx` fajl sintaksno ispravan, koristite textX komandu:
```bash
textx check grammar.tx
```

## Generisanje PNG vizualizacije gramatike
Za vizualizaciju strukture gramatike, potrebno je generisati DOT fajl i konvertovati ga u PNG:

1. **Generisanje DOT fajla iz textX gramatike:**
```bash
textx generate grammar.tx --target dot
```
Ova komanda generiše `grammar.dot` fajl koji opisuje strukturu gramatike.

2. **Konvertovanje DOT fajla u PNG:**
```bash
dot -Tpng -O grammar.dot
```
Ova komanda kreira `grammar.dot.png` fajl sa vizuelnim prikazom gramatike.

**Napomena:** Za generisanje slike potreban je Graphviz alat. Može se preuzeti sa [graphviz.org](https://graphviz.org/download/).

