//RNDQUOTE JOB (ACCT),'RANDOM QUOTE',CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//*
//* JOB VOOR HET UITVOEREN VAN DE REXX-SCRIPT
//*
//STEP1    EXEC PGM=IKJEFT01,DYNAMNBR=20
//SYSPRINT DD SYSOUT=*                    
//SYSTSPRT DD SYSOUT=*                    
//SYSIN    DD DUMMY                       
//SYSEXEC  DD DSN=&SYSUID..REXX,DISP=SHR   
//SYSTSIN  DD *                            
  %RANDOMQT
/*
//* COPY DE MOMENT QUOTE NAAR ZICHZELF OM DE STATUS BIJ TE WERKEN
//STEP2    EXEC PGM=IEBGENER
//SYSPRINT DD SYSOUT=*                   
//SYSUT1   DD DSN=&SYSUID..QUOTES.MOMENT,DISP=OLD
//SYSUT2   DD DSN=&SYSUID..QUOTES.MOMENT,DISP=SHR
//SYSIN    DD *
  OPTION COPY
/*

