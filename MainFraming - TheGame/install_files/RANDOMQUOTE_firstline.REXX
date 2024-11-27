/* REXX */
address TSO
say "Begin het proces om de eerste quote te selecteren."

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

/* Lees de eerste regel uit de dataset in de variabele 'firstQuote' */
say "Lees de eerste regel uit de dataset..."
"EXECIO 1 DISKR QUOTEDD (STEM firstQuote. FINIS"
if rc <> 0 then do
    say "Fout bij het lezen van de dataset " quoteFile
    say "Return code: " rc
    "FREE FI(QUOTEDD)"
    exit(8)
end
say "Eerste regel succesvol gelezen uit de dataset."

/* Sluit de QUOTES dataset */
"FREE FI(QUOTEDD)"
say "Dataset " quoteFile " succesvol vrijgegeven."

/* Controleer of er een quote is gelezen */
if firstQuote.0 = 0 then do
    say "Geen quotes beschikbaar in de dataset " quoteFile
    exit(8)
end

/* Toon de gelezen quote */
say "Gelezen quote: " firstQuote.1

/* Schrijf de eerste quote naar de QUOTES.MOMENT dataset */
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
randomQuote.1 = firstQuote.1
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
