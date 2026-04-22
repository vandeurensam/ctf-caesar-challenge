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

## 4. Development Process

### 4.1 Fase 1: Initiele Setup

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

### 4.2 Fase 2: Challenge Development

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

**Code Fragment:**
```python
# Gebruiker geeft shift-waarde in
shift = int(input("Enter shift value (0-25): "))

# Decrypt bericht
decrypted = caesar_decrypt(encrypted, shift)

# Check of correct
if shift == 3 and "The quick brown fox" in decrypted:
    print(f"FLAG: {FLAG}")  # Flag uit environment variable
```

**Prompts:**

Ik vroeg AI: *"hoe complete ik de eerste challenge ookalweer"*
- Resultaat: Gedetailleerde stap-voor-stap instructies

#### Challenge 2: Image Metadata (Forensics)
- **Type:** EXIF data extraction
- **Moeilijkheid:** Easy-Medium
- **Punten:** 150
- **Doelstelling:** Extract flag uit image metadata
- **Flag:** `CTF{3x1f_m3t4d4t4_5ecr3t}`

**Key Code:**
```python
# Create image met hidden flag in EXIF
exif_dict = {
    "0th": {
        piexif.ImageIFD.Software: FLAG.encode('utf-8'),
    }
}

# User voert 'help' in
if user_input == 'help':
    read_metadata_from_file()  # Toont alle EXIF data
```

#### Challenge 3: HTTP Headers & Cookies (Web Security)
- **Type:** Flask web app
- **Moeilijkheid:** Easy
- **Punten:** 100
- **Doelstelling:** Vind flag in HTTP headers/cookies
- **Flag:** `CTF{http_h34d3r_s3cr3t}`

**Key Code:**
```python
@app.route('/api/headers')
def api_headers():
    response = jsonify({"message": "Check the headers!"})
    response.headers['X-Flag-Part-1'] = 'CTF{'
    response.headers['X-Flag-Part-2'] = 'http_'
    # ... flag verdeeld over headers
    return response
```

### 4.3 Fase 3: Security & Best Practices

**Wat ik deed:**
- Verplaatste alle vlaggen uit code naar environment variables
- Maakte `.env.example` template
- Voegde `.env` toe aan `.gitignore`

**Prompt:** *"sla alle vlaggen op als docker envirement variable nooit als code"*

Resultaat: 
- ✓ Vlaggen nooit meer in code
- ✓ Environment variables via `.env` file
- ✓ `.env` beschermd tegen git commits

**Code Example:**
```python
# VOOR (slecht):
FLAG = "CTF{secret}"  # In code! NOOIT DOEN!

# NA (goed):
import os
FLAG = os.getenv('CAESAR_FLAG', 'default')  # Uit environment
```

### 4.4 Fase 4: Hints & Punten System

**Wat ik deed:**
- Voegde 4 hints toe per challenge
- Configureerde punten systeem
- Fixte flag type issues

**Prompts:**

1. *"heb je bij alle challenges al punten en hints erbij staan?"*
   - Resultaat: Scripts om hints in bulk toe te voegen

2. *"kan je ervoor zorgen dat je dan daadwerkelijk de punten krijgt en aan het scoreboard toevoegd?"*
   - Resultaat: `setup_scoring.py` en `fix_flag_types.py`

**Hint System:**
```python
hints_data = {
    "Caesar Cipher": [
        {
            "content": "A Caesar cipher shifts each letter...",
            "cost": 10  # Punten af voor hint
        },
        # ... meer hints
    ]
}
```

### 4.5 Fase 5: Docker Compose & Automation

**Wat ik deed:**
- Schreef `docker-compose.yml` voor alle containers
- Maakte `init_ctfd.py` voor auto-initialization
- Voegde health checks toe

**Prompt:** *"zorg dat alle containers starten via 1 commando: docker compose --build"*

Resultaat: `docker compose up --build` start alles!

**docker-compose.yml Highlights:**
```yaml
services:
  ctfd:
    image: ctfd/ctfd:latest
    env_file: .env  # Laadt vlaggen
    depends_on:
      - caesar-challenge
      - image-challenge
      - http-challenge

  caesar-challenge:
    build:
      dockerfile: Dockerfile.caesar
    env_file: .env  # Vlaggen beschikbaar
```

### 4.6 Fase 6: GitHub & Versiecontrol

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

## 5. Implementatie Details

### 5.1 Environment Variables & Security

**Probleem:** Vlaggen moeten secret blijven maar toegankelijk voor containers

**Oplossing:**
1. Maak `.env` file met vlaggen
2. `.env` in `.gitignore` (kan niet per ongeluk gecommit worden)
3. Share `.env.example` zonder echte vlaggen
4. Docker Compose laadt `.env` automatisch

**Bestand: .env**
```env
CAESAR_FLAG=CTF{c43s4r_c1ph3r_m4st3r}
IMAGE_METADATA_FLAG=CTF{3x1f_m3t4d4t4_5ecr3t}
HTTP_HEADERS_FLAG=CTF{http_h34d3r_s3cr3t}
```

**Bestand: .env.example** (Safe to share)
```env
# CTF Flags - Copy to .env and set your own flags
CAESAR_FLAG=CTF{your_caesar_flag}
IMAGE_METADATA_FLAG=CTF{your_image_flag}
HTTP_HEADERS_FLAG=CTF{your_http_flag}
```

### 5.2 Multi-Container Orchestration

**Probleem:** 4 services die moeten communiceren, dezelfde network nodig

**Oplossing:** Docker Compose network
```yaml
networks:
  ctf_network:
    driver: bridge

services:
  ctfd:
    networks:
      - ctf_network
  caesar-challenge:
    networks:
      - ctf_network
  # ... etc
```

### 5.3 Initialization & Scripting

**Probleem:** CTFd container moet weten over challenges en hints

**Oplossing:** `init_ctfd.py` script

```python
# Wacht tot database klaar is
def wait_for_db(max_retries=30):
    for attempt in range(max_retries):
        try:
            db.engine.execute("SELECT 1")
            return app
        except:
            time.sleep(1)

# Voeg challenges toe
for challenge_data in challenges_data:
    challenge = Challenges(
        name=challenge_data["name"],
        value=challenge_data["value"],
        # ...
    )
    db.session.add(challenge)
    db.session.commit()
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
Maakte `fix_flag_types.py`:
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
  ctfd:
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
$ echo "3" | docker run -it docker-caesar-challenge
Encrypted message: Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.
Enter shift value (0-25): 3
Decrypted: The quick brown fox jumps over the lazy dog.
CORRECT!
FLAG: CTF{c43s4r_c1ph3r_m4st3r}
```

**Result:** ✓ PASS

**Image Challenge Test:**
```bash
$ docker run -it docker-image-challenge
> help
EXIF Data Found:
  Software: CTF{3x1f_m3t4d4t4_5ecr3t}
```

**Result:** ✓ PASS

**HTTP Challenge Test:**
```bash
$ curl http://localhost:5000/api/inspect
{
  "flag": "CTF{http_h34d3r_s3cr3t}"
}
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
4. Submit: `CTF{3x1f_m3t4d4t4_5ecr3t}`
5. Check scoreboard → 150 points added (total: 250)

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
4. ✓ Web security (OWASP, headers, cookies)
5. ✓ Git & GitHub workflow
6. ✓ Environment variable security
7. ✓ Database interaction (SQLite via CTFd)
8. ✓ Project organization & documentation

**Ondanks AI gebruik:**
- Ik begrijp elke regel code
- Ik kan challenges aanpassen/uitbreiden
- Ik kan problemen debuggen
- Ik weet hoe Docker werkt

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

- [Docker Official Documentation](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/reference/)
- [CTFd GitHub](https://github.com/ctfdu/ctfd)
- [OWASP Security Top 10](https://owasp.org/www-project-top-ten/)
- [Python Best Practices](https://pep8.org/)

---

## Appendix C: AI Prompts Gebruikt

```
1. "i want to download CTFd via Docker"
2. "can you build a ctf challenge, Caesar cipher for example"
3. "kan je een github repository aanmaken en alle bestanden pushen"
4. "kan je nog 2 challenges toevoegen?: 1 vlag in metadata van een afbeelding (Exiftool) 
   en 1 verstop een vlag in een http header of cookie via flask"
5. "sla alle vlaggen op als docker envirement variable nooit als code"
6. "heb je bij alle challenges al punten en hints erbij staan?"
7. "zorg dat alle containers starten via 1 commando: docker compose --build"
8. "kan je ervoor zorgen dat je dan daadwerkelijk de punten krijgt en aan het scoreboard toevoegd?"
9. "kan je een realisatie bestand maken voor alles wat we tot nu toe hebben gedaan?"
```

---

**Einde Realisatierapport**

*Datum: April 2026*  
*Auteur: [Jouw Naam]*  
*Begeleider: [Begeleider Naam]*  
*School: [School Naam]*
