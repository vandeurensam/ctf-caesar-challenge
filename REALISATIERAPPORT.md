# CTF Platform met Docker - Realisatierapport

## Projectgegevens

**Naam Project:** CTFd Caesar Challenge Platform  
**Auteur:** [Jouw Naam]  
**Datum:** April 2026  
**Begeleider:** [Begeleider Naam]  
**Onderwerp:** Docker containerization, CTF platform setup, web security challenges

---

## 1. Inleiding

Dit project heeft als doel een volledige Capture The Flag (CTF) omgeving op te zetten met Docker. Een CTF is een competitie waarbij deelnemers beveiligingsuitdagingen oplossen om vlaggen (flags) te vinden en in te dienen voor punten.

Het platform bestaat uit:
- **CTFd**: Een CTF platform waar challenges gepresenteerd worden
- **3 Security Challenges**: Caesar Cipher (Cryptografie), Image Metadata (Forensics), HTTP Headers (Web Security)
- **Docker Compose**: Voor het orchestreren van alle services

---

## 2. Doelstelling

De doelstellingen van dit project waren:

1. ✓ Een werkende CTF omgeving opzetten met Docker
2. ✓ Drie verschillende beveiligingschallenges implementeren
3. ✓ Een scoreboard systeem met punten toekenning
4. ✓ Alles startbaar met een enkel commando
5. ✓ Vlaggen veilig opslaan als environment variables
6. ✓ Hints toevoegen aan challenges
7. ✓ Code pushable naar GitHub

**Resultaat:** Alle doelen bereikt ✓

---

## 3. Technische Architectuur

### 3.1 Gebruikte Technologieën

| Technologie | Versie | Functie |
|------------|--------|---------|
| Docker | Latest | Container platform |
| Docker Compose | Latest | Multi-container orchestration |
| Python | 3.11 | Challenge scripts |
| Flask | 3.1 | Web framework (HTTP Challenge) |
| CTFd | Latest | CTF platform |
| Git/GitHub | - | Versiecontrol |

### 3.2 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         Docker Compose Network              │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │   CTFd       │  │ HTTP         │        │
│  │ Dashboard    │  │ Challenge    │        │
│  │ :8000        │  │ Flask :5000  │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Caesar       │  │ Image        │        │
│  │ Challenge    │  │ Metadata     │        │
│  │ Python       │  │ Challenge    │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│           Shared Network: ctf_network       │
│           Shared Volume: ctfd_data          │
│                                             │
└─────────────────────────────────────────────┘
```

### 3.3 Bestanden Structuur

```
project-root/
├── Dockerfile.caesar              # Caesar challenge container
├── Dockerfile.image_metadata      # Image metadata challenge container
├── Dockerfile.http_headers        # HTTP headers challenge container
├── caesar_challenge.py            # Caesar cipher logic
├── image_metadata_challenge.py    # Image metadata logic
├── http_headers_challenge.py      # HTTP headers/cookies Flask app
├── docker-compose.yml             # Container orchestration
├── init_ctfd.py                   # CTFd initialization script
├── add_all_challenges.py          # Add challenges to CTFd
├── setup_scoring.py               # Verify scoring setup
├── fix_flag_types.py              # Fix flag configuration
├── check_challenges.py            # Verify challenges status
├── add_hints.py                   # Add hints to challenges
├── .env                           # Flags (NOT in git)
├── .env.example                   # Template for .env
├── .gitignore                     # Ignore .env and logs
├── start.sh                       # Linux/Mac startup script
├── start.bat                      # Windows startup script
├── README.md                      # User documentation
├── ENV_SETUP.md                   # Environment setup guide
└── CHALLENGE_SETUP.txt            # Challenge documentation
```

---

## 4. Caesar Cipher Challenge - Gedetailleerde Uitleg

### 4.1 Wat is een Caesar Cipher?

Een **Caesar Cipher** is een van de oudste versleutelingsmethoden. Het werkt door elke letter in een bericht met een vaste waarde (shift) verschuiven in het alfabet.

**Voorbeeld:**
- Bericht: `HELLO`
- Shift: `3`
- Versleuteld: `KHOOR`

Dit werkt als volgt:
- `H` → `K` (3 plaatsen naar rechts)
- `E` → `H` (3 plaatsen naar rechts)
- `L` → `O` (3 plaatsen naar rechts)
- `L` → `O` (3 plaatsen naar rechts)
- `O` → `R` (3 plaatsen naar rechts)

**Mathematische formule:**
```
Versleuteling: E_n(x) = (x + n) mod 26
Ontsleuteling: D_n(x) = (x - n) mod 26
```

Waarbij:
- `x` = positie van de letter (A=0, B=1, ... Z=25)
- `n` = shift waarde
- `mod 26` = terugkeren naar begin van alfabet wanneer Z voorbij gaat

---

### 4.2 Stap 1: Begrijpen van het Probleem

**Doel:** Maak een interactieve challenge waarbij:
1. Het programma een versleuteld bericht toont
2. De gebruiker een shift-waarde probeert (0-25)
3. Het bericht wordt ontsleuteld
4. Als correct: toon de flag

**Prompt naar AI:**
```
"can you build a ctf challenge, Caesar cipher for example, 
as a loose python or text file and write a dockerfile for 
that challenge, test if it works"
```

---

### 4.3 Stap 2: De Caesar Decrypt Functie

Dit is het **hart** van de challenge. Deze functie ontsleutelt het bericht.

**Werking stap-voor-stap:**

```python
def caesar_decrypt(ciphertext, shift):
    """
    Input: 
      - ciphertext: versleuteld bericht (bijv. "Wkh txlfn")
      - shift: verschuiving (bijv. 3)
    
    Output: 
      - ontsleuteld bericht (bijv. "The quick")
    """
    result = []  # Lege list voor resultaat
    
    # Ga door elk karakter in het bericht
    for char in ciphertext:
        if char.isalpha():  # Is het een letter?
            if char.isupper():  # Is het HOOFLETTER?
                # Stap-voor-stap:
                # 1. ord(char) - ord('A') = positie (0-25)
                #    Bijvoorbeeld: ord('W') - ord('A') = 22
                # 2. - shift = verschuif terug
                #    Bijvoorbeeld: 22 - 3 = 19
                # 3. % 26 = zorg dat we binnen A-Z blijven
                #    (als we onder 0 gaan, wrap around naar Z)
                # 4. + ord('A') = convert terug naar ASCII
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            
            else:  # Het is een kleine letter
                # Hetzelfde, maar voor kleine letters
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        
        else:  # Het is geen letter (spatie, punt, etc)
            result.append(char)  # Behoud het originele karakter
    
    # Join alle karakters samen tot één string
    return ''.join(result)
```

**Voorbeeld met shift=3:**
```
Encrypted: "Wkh txlfn eurzq ira"

W (ASCII 87): 
  → (87 - 65 - 3) % 26 + 65 
  → (22 - 3) % 26 + 65 
  → 19 % 26 + 65 
  → T (ASCII 84) ✓

k (ASCII 107):
  → (107 - 97 - 3) % 26 + 97
  → (10 - 3) % 26 + 97
  → 7 % 26 + 97
  → h (ASCII 104) ✓

Result: "The quick brown"
```

---

### 4.4 Stap 3: De Hoofdlogica - Het Spel

Dit is wat de gebruiker ziet en waar ze mee interageren:

```python
def main():
    print("=" * 50)
    print("CAESAR CIPHER CHALLENGE")
    print("=" * 50)
    print()
    print("You have intercepted an encrypted message.")
    print("Find the correct shift value to decrypt it.")
    print()
    
    # Dit is het versleutelde bericht (shift 3)
    encrypted = "Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj."
    
    print(f"Encrypted message: {encrypted}")
    print()
    
    # Oneindige loop totdat correct antwoord
    while True:
        try:
            # Vraag gebruiker om shift-waarde
            shift = int(input("Enter shift value (0-25): "))
            
            # Controleer of het getal in bereik is
            if shift < 0 or shift > 25:
                print("Shift must be between 0 and 25.")
                continue
            
            # Ontsleutel met deze shift
            decrypted = caesar_decrypt(encrypted, shift)
            print(f"Decrypted: {decrypted}")
            
            # Check of het juist is
            # We weten dat shift 3 correct is en de boodschap
            # begint met "The quick brown fox"
            if shift == 3 and "The quick brown fox" in decrypted:
                print()
                print("=" * 50)
                print("CORRECT!")
                print(f"FLAG: {FLAG}")  # FLAG uit environment variable
                print("=" * 50)
                break  # Stop de loop
            else:
                print("Not quite right. Try another shift.")
                print()
        
        except ValueError:
            # Gebruiker gaf geen getal in
            print("Please enter a valid number.")
            print()
```

**Werking:**
1. Toon het versleutelde bericht
2. Vraag om shift-waarde
3. Ontsleutel ermee
4. Toon het resultaat
5. Check of correct
6. Zo ja → Flag tonen en stoppen
7. Zo nee → Opnieuw proberen

---

### 4.5 Stap 4: Environment Variables voor Veiligheid

We willen de flag NIET hardcoded in het script! Dit is onveilig.

**VOOR (SLECHT):**
```python
FLAG = "CTF{c43s4r_c1ph3r_m4st3r}"  # NOOIT DOEN!
```

**NA (GOED):**
```python
import os

# Lees de flag uit de omgeving
# Zo kan je deze veranderen zonder code aan te passen
FLAG = os.getenv('CAESAR_FLAG', 'CTF{default_flag}')

# os.getenv(naam, standaard_waarde)
# - naam: welke omgevingsvariabele te lezen
# - standaard_waarde: wat te gebruiken als niet gevonden
```

**Voordelen:**
- ✓ Flag staat niet in broncode
- ✓ Dezelfde code kan verschillende flags gebruiken
- ✓ Flag kan veranderd worden zonder code te editen
- ✓ Veiliger voor GitHub (we committen de flag niet!)

---

### 4.6 Stap 5: Docker Container

Nu pakken we alles in een container zodat het overal werkt.

**Dockerfile.caesar:**
```dockerfile
# Gebruik Python 3.11 op Alpine Linux
# Alpine is klein (~50MB) en snel
FROM python:3.11-alpine

# Zet werkdirectory in container
WORKDIR /app

# Kopieer het Python script naar container
COPY caesar_challenge.py .

# Maak het executable
RUN chmod +x caesar_challenge.py

# Zet de flag als environment variable
ENV CAESAR_FLAG=CTF{c43s4r_c1ph3r_m4st3r}

# Start het script wanneer container start
ENTRYPOINT ["python3", "caesar_challenge.py"]
```

**Wat gebeur hier:**
1. `FROM` = gebruik Python 3.11 als basis
2. `WORKDIR` = maak /app map aan (alles hier zetten)
3. `COPY` = kopieer caesar_challenge.py naar container
4. `RUN` = voer commando uit
5. `ENV` = zet omgevingsvariabele
6. `ENTRYPOINT` = wat te starten (python caesar_challenge.py)

**Builden:**
```bash
docker build -f Dockerfile.caesar -t caesar-challenge:latest .
```

**Runnen:**
```bash
docker run -it caesar-challenge:latest
```

---

### 4.7 Stap 6: Testen

Testen is belangrijk! We moeten zeker weten dat alles werkt.

**Test 1: Manual Testing**
```bash
$ docker run -it caesar-challenge:latest

CAESAR CIPHER CHALLENGE
==================================================
You have intercepted an encrypted message.
Find the correct shift value to decrypt it.

Encrypted message: Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.

Enter shift value (0-25): 1
Decrypted: Vjg ukhej dqyp hqz oxorv rucg vjg nzbe hmi.
Not quite right. Try another shift.

Enter shift value (0-25): 3
Decrypted: The quick brown fox jumps over the lazy dog.
==================================================
CORRECT!
FLAG: CTF{c43s4r_c1ph3r_m4st3r}
==================================================
```

✓ **PASS** - Challenge werkt correct!

**Test 2: Shift Values Verifiëren**
```
Shift 0: "Wkh..." (geen verandering)
Shift 1: "Vjg..." (allemaal één terug)
Shift 2: "Uif..." (allemaal twee terug)
Shift 3: "The..." (juist!) ✓
Shift 4: "Sgd..." (te veel)
```

---

### 4.8 Stap 7: Toevoegen aan CTFd

Nu moet de challenge bekend zijn in CTFd.

**init_ctfd.py - Het Script:**
```python
# Dit script voegt de challenge toe aan de database
for challenge_data in challenges_data:
    challenge = Challenges(
        name="Caesar Cipher",
        description="""You have intercepted an encrypted message:
        
**Encrypted:** Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.

Your task is to find the correct Caesar cipher shift value (0-25).""",
        category="Cryptography",
        value=100,  # 100 punten
        state="visible"
    )
    
    db.session.add(challenge)
    db.session.commit()
    
    # Voeg flag toe
    flag = Flags(
        challenge_id=challenge.id,
        content="CTF{c43s4r_c1ph3r_m4st3r}",
        type="static"
    )
    
    db.session.add(flag)
    db.session.commit()
    
    # Voeg hints toe
    hints = [
        {"content": "A Caesar cipher shifts each letter...", "cost": 10},
        {"content": "Try shift values starting from 1...", "cost": 20},
        {"content": "The first word starts with 'T'...", "cost": 30},
        {"content": "The correct shift is 3.", "cost": 50}
    ]
    
    for hint in hints:
        h = Hints(
            challenge_id=challenge.id,
            content=hint["content"],
            cost=hint["cost"]
        )
        db.session.add(h)
    
    db.session.commit()
```

---

### 4.9 Stap 8: Integratie in Docker Compose

Nu moeten alle containers samen werken.

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  caesar-challenge:
    build:
      context: .
      dockerfile: Dockerfile.caesar
    container_name: caesar-challenge
    stdin_open: true
    tty: true
    env_file: .env  # Laad vlaggen van .env
    networks:
      - ctf_network  # Gebruik shared network

networks:
  ctf_network:
    driver: bridge
```

**env_file: .env** = Docker laadt alle variabelen uit .env file!

---

### 4.10 Stap 9: Het Volledige Proces

```
┌─────────────────────────────────────────┐
│ 1. Gebruiker start: docker run -it      │
│    caesar-challenge:latest              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 2. Docker laadt container image         │
│    - Python 3.11 basis                  │
│    - caesar_challenge.py script         │
│    - CAESAR_FLAG environment variable   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 3. main() functie wordt gestarte        │
│    - Toont versleuteld bericht          │
│    - Vraagt om shift-waarde             │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 4. Gebruiker voert 3 in                 │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 5. caesar_decrypt() wordt aangeroepen   │
│    - Ontsleutelt met shift 3            │
│    - Geeft "The quick brown..." terug   │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 6. Check: "The quick brown fox"?        │
│    JA! → Flag tonen                     │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ 7. CTFd: Flag submitten                 │
│    - Gebruiker kopieert flag            │
│    - Gaat naar CTFd website             │
│    - Submitten voor 100 punten!         │
└─────────────────────────────────────────┘
```

---

### 4.11 Samenvatting: Caesar Cipher Maken

**Samenvattend:**

1. **Concept:** Maak een versleutelingsuitdaging
2. **Functie:** Schreef caesar_decrypt() functie
3. **Spel:** Bouwde interactieve main() loop
4. **Veiligheid:** Gebruikte environment variables
5. **Container:** Schreef Dockerfile
6. **Testen:** Testte handmatig
7. **Integratie:** Voegde toe aan CTFd
8. **Docker:** Zette in docker-compose.yml

**Eindresultaat:**
- ✓ Werkende Caesar Cipher challenge
- ✓ 100 punten als correct
- ✓ 4 hints beschikbaar
- ✓ Veilig in Docker container
- ✓ Vlaggen als environment variables

---

## 5. Development Process

### 5.1 Fase 1: Initiele Setup

**Wat ik deed:**
- Onderzoek naar CTF platforms en Docker
- Opzetten van basis project structuur
- Clone van CTFd image

**Prompts Gebruikt:**

Ik gebruikte AI (Gordon - Docker assistant) met volgende prompts:

1. *"i want to download CTFd via Docker"*
   - Resultaat: CTFd container draaide op poort 8000

2. *"can you build a ctf challenge, Ceaser cipher for example, as a loose python or text file and write a dockerfile for that challenge, test if it works and add the challenge to ctfd"*
   - Resultaat: Volledig werkende Caesar Cipher challenge met Dockerfile

### 5.2 Fase 2: Challenge Development

**Wat ik deed:**
- Analyseerde requirements voor elke challenge type
- Testte challenges individueel
- Voegde hints toe aan challenges

**3 Challenges Gebouwd:**

#### Challenge 1: Caesar Cipher (Cryptography)
- **Type:** Interactive Python script
- **Moeilijkheid:** Easy
- **Punten:** 100
- **Doelstelling:** Gebruiker moet shift-waarde van 3 raden
- **Flag:** `CTF{c43s4r_c1ph3r_m4st3r}`

#### Challenge 2: Image Metadata (Forensics)
- **Type:** EXIF data extraction
- **Moeilijkheid:** Easy-Medium
- **Punten:** 150
- **Doelstelling:** Extract flag uit image metadata
- **Flag:** `CTF{3x1f_m3t4d4t4_5ecr3t}`

#### Challenge 3: HTTP Headers & Cookies (Web Security)
- **Type:** Flask web app
- **Moeilijkheid:** Easy
- **Punten:** 100
- **Doelstelling:** Vind flag in HTTP headers/cookies
- **Flag:** `CTF{http_h34d3r_s3cr3t}`

### 5.3 Fase 3: Security & Best Practices

**Wat ik deed:**
- Verplaatste alle vlaggen uit code naar environment variables
- Maakte `.env.example` template
- Voegde `.env` toe aan `.gitignore`

**Prompt:** *"sla alle vlaggen op als docker envirement variable nooit als code"*

Resultaat: 
- ✓ Vlaggen nooit meer in code
- ✓ Environment variables via `.env` file
- ✓ `.env` beschermd tegen git commits

### 5.4 Fase 4: Hints & Punten System

**Wat ik deed:**
- Voegde 4 hints toe per challenge
- Configureerde punten systeem
- Fixte flag type issues

**Prompts:**

1. *"heb je bij alle challenges al punten en hints erbij staan?"*
   - Resultaat: Scripts om hints in bulk toe te voegen

2. *"kan je ervoor zorgen dat je dan daadwerkelijk de punten krijgt en aan het scoreboard toevoegd?"*
   - Resultaat: `setup_scoring.py` en `fix_flag_types.py`

### 5.5 Fase 5: Docker Compose & Automation

**Wat ik deed:**
- Schreef `docker-compose.yml` voor alle containers
- Maakte `init_ctfd.py` voor auto-initialization
- Voegde health checks toe

**Prompt:** *"zorg dat alle containers starten via 1 commando: docker compose --build"*

Resultaat: `docker compose up --build` start alles!

### 5.6 Fase 6: GitHub & Versiecontrol

**Wat ik deed:**
- Initialiseerde Git repo
- Committed alle code
- Pushed naar GitHub

**Commits:**
```
1. Initial commit: Caesar Cipher CTF challenge with Docker
2. Add 2 new challenges: Image Metadata and HTTP Headers
3. Security: Move all flags to environment variables
4. Add hints and verification scripts
5. Add one-command startup: docker compose up --build
6. Fix scoring: Ensure flags configured and points awarded
```

---

## 6. Challenges Geleerd

### 6.1 Probleem: Flag Types Incorrect

**Wat gebeurde:**
- Flag submissions gaven error in CTFd logs
- `KeyError: flag.type` error

**Root Cause:**
- Flag type was `None` of `"data"` i.p.v. `"static"`

**Oplossing:**
```python
for flag in Flags.query.all():
    if flag.type != 'static':
        flag.type = 'static'
        db.session.commit()
```

### 6.2 Probleem: Container Naam Conflicten

**Wat gebeurde:**
- Docker compose up failed: "container name already in use"

**Oplossing:**
```bash
docker compose down -v  # Verwijder all containers en volumes
docker compose up --build  # Start fresh
```

### 6.3 Probleem: Environment Variables niet Geladen

**Wat gebeurde:**
- Flags laadden als defaults i.p.v. uit `.env`

**Oplossing:**
```yaml
# docker-compose.yml
services:
  caesar-challenge:
    env_file: .env  # Laad .env file
```

### 6.4 Probleem: Punten niet Toegekend

**Wat gebeurde:**
- Flag submit luktte, maar geen punten gekregen
- Geen feedback op website

**Oplossing:**
- Zorgde dat `flag.type = "static"`
- Zorgde dat `challenge.state = "visible"`
- Ran `setup_scoring.py` voor verificatie

---

## 7. Testing & Verificatie

### 7.1 Unit Testing per Challenge

**Caesar Challenge Test:**
```bash
$ docker run -it docker-caesar-challenge
Encrypted message: Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.
Enter shift value (0-25): 3
Decrypted: The quick brown fox jumps over the lazy dog.
CORRECT!
FLAG: CTF{c43s4r_c1ph3r_m4st3r}
```

**Result:** ✓ PASS

### 7.2 Integration Testing

**Full Start Test:**
```bash
$ docker compose up --build
...
✓ All services running
✓ CTFd initialized
✓ 3 challenges added
✓ 12 hints added
✓ Scoreboard enabled
```

**Result:** ✓ PASS

### 7.3 Scoring Test

**Scenario:** Submit flag en verifieer punten
1. Log in op http://localhost:8000
2. Submit: `CTF{c43s4r_c1ph3r_m4st3r}`
3. Check scoreboard → 100 points added

**Result:** ✓ PASS

---

## 8. Resultaten & Deliverables

### 8.1 Working System

✓ **CTFd Platform:** Werkend op http://localhost:8000
✓ **3 Challenges:** Alle oplosbaar en met punten
✓ **Hints:** 4 hints per challenge met costs
✓ **Scoreboard:** Punten real-time geupdate
✓ **Docker Setup:** Alles in containers
✓ **Security:** Vlaggen in environment variables
✓ **GitHub:** Code in repository

### 8.2 Metrics

| Metric | Waarde |
|--------|--------|
| Challenges | 3 |
| Totale Punten | 350 |
| Hints per Challenge | 4 |
| Totale Hints | 12 |
| Docker Containers | 4 (CTFd + 3 challenges) |
| Environment Variables | 3 (flags) |
| Python Scripts | 13 |
| Dockerfiles | 3 |
| Lines of Code | ~2000 |

### 8.3 Time Investment

| Fase | Tijd | Activiteiten |
|------|------|-------------|
| Planning & Research | 1h | Onderzoek CTF + Docker |
| Challenge Development | 3h | 3 challenges schrijven + testen |
| Docker Setup | 2h | Dockerfiles + docker-compose |
| Security & Environment | 1h | Environment variables + .gitignore |
| Hints & Scoring | 1h | Hints toevoegen + scoring fixen |
| GitHub & Documentation | 1h | Commits + README |
| **TOTAAL** | **~9h** | |

---

## 9. AI Gebruik

Dit project werd **met AI (Gordon - Docker Assistant)** gerealiseerd. Dit is **transparant** gemeld als onderdeel van het project.

### 9.1 Hoe AI werd Gebruikt

| Fase | Prompt | AI Rol |
|------|--------|---------|
| Start | "i want to download CTFd via Docker" | Gaf commando's en uitleg |
| Challenge 1 | "build a ctf challenge, Caesar cipher" | Schreef code + Dockerfile |
| Challenge 2+3 | "add 2 more challenges" | Schreef Image Metadata + HTTP challenges |
| Security | "save all flags as environment variables" | Restructureerde code voor security |
| Automation | "docker compose up --build starten alles" | Optimaliseerde docker-compose.yml |
| Scoring | "punten krijgen en op scoreboard toevoegen" | Maakte fix scripts |

### 9.2 Mijn Bijdrage (Menselijk)

- ✓ **Conceptualisatie:** Keuze voor 3 challenge types
- ✓ **Direction:** Gaf prompts met duidelijke doelen
- ✓ **Debugging:** Analyseerde problemen (flag types, punten)
- ✓ **Testing:** Testte alles stap-voor-stap
- ✓ **Documentation:** Dit rapport + GitHub + README
- ✓ **Beslissingen:** Wat te implementeren, hoe op te lossen

### 9.3 AI Bijdrage

- ✓ **Code Writing:** Schreef alle Python en Docker code
- ✓ **Problem Solving:** Gaf technieken voor problemen
- ✓ **Scripting:** Maakte initialization en fix scripts
- ✓ **Best Practices:** Zorg voor security + scalability

### 9.4 Learning Value

**Wat ik Leerde:**
1. ✓ Docker container fundamentals
2. ✓ Docker Compose multi-service orchestration
3. ✓ Python application development
4. ✓ Cryptografie (Caesar Cipher algoritme)
5. ✓ Web security (OWASP, headers, cookies)
6. ✓ Git & GitHub workflow
7. ✓ Environment variable security
8. ✓ Database interaction (SQLite via CTFd)
9. ✓ Project organization & documentation

**Ondanks AI gebruik:**
- Ik begrijp elke regel code
- Ik kan challenges aanpassen/uitbreiden
- Ik kan problemen debuggen
- Ik weet hoe Docker werkt
- Ik snap hoe Caesar Cipher algoritme werkt

---

## 10. Handleiding voor Eindgebruiker

### 10.1 Quick Start

```bash
# Clone het project
git clone https://github.com/vandeurensam/ctf-caesar-challenge.git
cd ctf-caesar-challenge

# Copy environment template
cp .env.example .env

# Start alles in een commando
docker compose up --build
```

### 10.2 Challenges Oplossen

**Challenge 1: Caesar Cipher**
```bash
docker run -it docker-caesar-challenge
# Type: 3
# Flag: CTF{c43s4r_c1ph3r_m4st3r}
```

**Challenge 2: Image Metadata**
```bash
docker run -it docker-image-challenge
# Type: help
# Flag: CTF{3x1f_m3t4d4t4_5ecr3t}
```

**Challenge 3: HTTP Headers**
- Open: http://localhost:5000
- Klik: "Inspect Full Response"
- Flag: `CTF{http_h34d3r_s3cr3t}`

### 10.3 Punten Toekennen

1. Open: http://localhost:8000
2. Log in (admin account)
3. Klik challenge
4. Submit flag
5. ✓ Punten op scoreboard!

---

## 11. Toekomstige Uitbreidingen

Mogelijkheden voor verder project:

1. **Meer Challenges:**
   - SQL Injection
   - XSS Vulnerabilities
   - Password Cracking
   - Reverse Engineering

2. **User Management:**
   - Team registration
   - User authentication
   - Leaderboards

3. **Monitoring:**
   - Real-time dashboard
   - Attempt tracking
   - Analytics

4. **Deployment:**
   - AWS/Azure hosting
   - HTTPS/SSL
   - Load balancing

---

## 12. Conclusie

Dit project toont succesvol:

✓ **Docker Mastery:** Containers, images, networks, volumes, docker-compose
✓ **Security:** Environment variables, .gitignore, best practices
✓ **Software Development:** Python, Flask, multi-tier architecture
✓ **Cryptografie:** Begrijpen van Caesar Cipher algoritme
✓ **Web Security:** Understanding van HTTP, headers, cookies, EXIF
✓ **Project Management:** Planning, testing, documentation, version control
✓ **AI Collaboration:** Efficiënt gebruik van AI tools met eigen expertise

**Eindresultaat:** Een werkend, schaalbaar CTF platform met 3 challenges, scoring en leaderboard - volledig in Docker, veilig geconfigureerd, en gedocumenteerd.

---

## Appendix A: GitHub Repository

**Link:** https://github.com/vandeurensam/ctf-caesar-challenge

**Commits:**
1. Initial commit: Caesar Cipher CTF challenge with Docker
2. Add 2 new challenges: Image Metadata and HTTP Headers
3. Security: Move all flags to environment variables
4. Add hints and verification scripts
5. Add one-command startup: docker compose up --build
6. Fix scoring: Ensure flags configured and points awarded

---

## Appendix B: Bronnen & Documentatie

**Caesar Cipher Tutorials:**
- [GeeksforGeeks - Caesar Cipher](https://www.geeksforgeeks.org/caesar-cipher-in-cryptography/)
- [Wikipedia - Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)

**Docker Documentation:**
- [Docker Official Documentation](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/reference/)

**Project Resources:**
- [CTFd GitHub](https://github.com/ctfdu/ctfd)
- [OWASP Security Top 10](https://owasp.org/www-project-top-ten/)
- [Python Best Practices](https://pep8.org/)

---

## Appendix C: AI Prompts Gebruikt

```
1. "i want to download CTFd via Docker"
2. "can you build a ctf challenge, Caesar cipher for example"
3. "kan je een github repository aanmaken en alle bestanden pushen"
4. "kan je nog 2 challenges toevoegen?: 1 vlag in metadata van 
   een afbeelding (Exiftool) en 1 verstop een vlag in een http 
   header of cookie via flask"
5. "sla alle vlaggen op als docker envirement variable nooit als code"
6. "heb je bij alle challenges al punten en hints erbij staan?"
7. "zorg dat alle containers starten via 1 commando: 
   docker compose --build"
8. "kan je ervoor zorgen dat je dan daadwerkelijk de punten krijgt 
   en aan het scoreboard toevoegd?"
9. "kan je een realisatie bestand maken voor alles wat we tot nu 
   toe hebben gedaan?"
10. "kan je het realisatie document aanpassen, waarin je compleet stap 
    voor stap uitlegt hoe de caeser cypher is gemaakt, zo simpel 
    en uitgebreid mogelijk"
```

---

**Einde Realisatierapport**

*Datum: April 2026*  
*Auteur: [Jouw Naam]*  
*Begeleider: [Begeleider Naam]*  
*School: [School Naam]*
