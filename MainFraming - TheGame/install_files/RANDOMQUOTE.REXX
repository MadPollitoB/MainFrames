/* REXX */
address TSO
say "Begin het proces om een willekeurige quote te selecteren."

/* Haal de gebruikers-ID op van de huidige gebruiker */
userID = sysvar("SYSUID")
say "Gebruikers-ID opgehaald: " userID

/* Open de QUOTES dataset en lees de inhoud */
quoteFile = "'"userID".QUOTES'"  /* Dataset naam met dynamische userID */
say "Probeer dataset te openen: " quoteFile

/* Allocate the dataset to a DDNAME */
"ALLOC FI(QUOTEDD) DA("quoteFile") SHR"
if rc <> 0 then do
    say "Fout bij het alloceren van de dataset " quoteFile
    say "Return code: " rc
    exit(8)
end
say "Dataset succesvol gealloceerd: " quoteFile

/* Lees alle regels uit de dataset in de variabele 'quotes' */
say "Lees alle regels uit de dataset..."
"EXECIO * DISKR QUOTEDD (STEM quotes. FINIS"
if rc <> 0 then do
    say "Fout bij het lezen van de dataset " quoteFile
    say "Return code: " rc
    "FREE FI(QUOTEDD)"
    exit(8)
end
say "Alle regels succesvol gelezen uit de dataset."

/* Sluit de QUOTES dataset */
"FREE FI(QUOTEDD)"
say "Dataset " quoteFile " succesvol vrijgegeven."

/* Controleer of er quotes zijn gelezen */
if quotes.0 = 0 then do
    say "Geen quotes beschikbaar in de dataset " quoteFile
    exit(8)
end

/* Selecteer een willekeurige quote */
say "Selecteer een willekeurige quote uit de dataset..."
quoteCount = quotes.0

/* Gebruik RANDOM() functie van REXX om een index te genereren */
call time 'S'
seed = time('S') /* Haal de huidige seconden op als seed */
randomIndex = 1 + random(seed) // quoteCount 
randomQuote = quotes.randomIndex
say "Geselecteerde willekeurige quote: " randomQuote

/* Schrijf de willekeurige quote naar de QUOTES.MOMENT dataset */
momentFile = "'"userID".QUOTES.MOMENT'"
say "Probeer dataset te openen voor schrijven: " momentFile

/* Allocate the dataset to a DDNAME */
"ALLOC FI(MOMENTDD) DA("momentFile") SHR"
if rc <> 0 then do
    say "Fout bij het alloceren van de dataset " momentFile
    say "Return code: " rc
    exit(8)
end
say "Dataset succesvol gealloceerd voor schrijven: " momentFile

/* We gebruiken EXECIO om de quote te schrijven */
randomQuote.1 = randomQuote
say "Probeer de quote te schrijven naar de dataset..."
"EXECIO 1 DISKW MOMENTDD (STEM randomQuote. FINIS"
if rc <> 0 then do
    say "Fout bij het schrijven naar de dataset " momentFile
    say "Return code: " rc
    "FREE FI(MOMENTDD)"
    exit(8)
end
say "Quote succesvol geschreven naar de dataset."

/* Sluit de QUOTES.MOMENT dataset */
"FREE FI(MOMENTDD)"
say "Dataset " momentFile " succesvol vrijgegeven."

say "Willekeurige quote toegevoegd!"
exit(0)
