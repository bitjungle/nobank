# nobank - Norsk ordbank (bokmål) med verktøy

Kildefilene for ord-databasen er hentet fra 
[Nasjonalbiblioteket](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/), 
og har lisensen [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Beskrivelse av ordbanken

Norsk ordbank – bokmål 2005 er en leksikalsk database som reflekterer rettskrivningsreformen 
som ble effektuert 1. juli 2005 og senere justeringer av rettskrivningen for bokmål. Databasen 
er sammensatt av en grunnordliste og et sett av bøyningsmønstre. Hvert ord i grunnordlisten har 
ett eller flere bøyningsmønstre. Hvert bøyningsmønster inneholder en linje for hver enkelt bøyde 
form av grunnordet. En linje inneholder et omformingsmønster og informasjon om ordklasse og 
morfologiske trekk. Mønsteret viser hvordan grunnordet kan ekspanderes til en bøyd form. Dataene 
er lagret i sju tabeller. Tabellen «lemma» inneholder alle oppslagsordene i Bokmålsordboka med 
spesifikasjon av artikkelnummeret. Fullformslisten inneholder alle mulige bøyde former av 
oppslagsordene i tråd med gjeldende rettskrivning. Denne tabellen inneholder også former som er 
tenkelige, men i praksis brukes sjelden eller aldri, f.eks. flertallsformer som "snøer" og 
sammensetninger som "løvskau". Tabellene «lemma_paradigme», «paradigme», «paradigme_boying», 
«boying_grupper» og «boying» inneholder den informasjonen som er nødvendig for å generere 
fullformene basert på grunnordlisten («lemma»). De inneholder med andre ord koblingen mellom 
grunnord og bøyningsmønster, regler og informasjon om kategorier. Tabellen «leddanalyse» 
inneholder informasjon om leddeling av sammensetninger. I Bokmålsordboka er leddelingen markert 
med en vertikal strek: bank|boks. Fullformslisten inneholder informasjon om argumentstruktur for 
en del verb. De ulike kodene som er brukt, beskrives i filen «Norsk_ordbank_argstr.txt». 
Dokumentasjonsfilen gjør rede for strukturen i dataene. Legg merke til at dette er en dump av 
databasen slik den forelå 1. februar 2022. En søkbar og oppdatert versjon av Norsk ordbank 
finnes hos Språksamlingane ved Universitetsbiblioteket i Bergen. Den siste versjonen 
(1. februar 2022) inneholder 154.824 lemma.

