# CTFd Caesar Cipher Challenge

Een volledige CTF (Capture The Flag) setup met CTFd en een interactieve Caesar cipher cryptografie challenge.

## 📋 Inhoud

- **CTFd**: Een open-source CTF platform
- **Caesar Cipher Challenge**: Een Docker container met een interactieve cryptografie challenge
- **Docker Compose**: Eenvoudige setup voor beide services

## 🚀 Quick Start

### Vereisten
- Docker en Docker Compose geïnstalleerd

### Optie 1: Docker Compose (Aanbevolen)

```bash
git clone <repository-url>
cd ctf-caesar-challenge
docker compose up -d
```

Open http://localhost:8000 in je browser.

### Optie 2: Handmatig

```bash
# Start CTFd
docker run -d --name ctfd -p 8000:8000 ctfd/ctfd

# Build en run de Caesar challenge
docker build -f Dockerfile.caesar -t caesar-cipher-challenge:latest .
docker run -it caesar-cipher-challenge:latest
```

## 🎯 Challenge Oplossen

### De Challenge

Je hebt een versleuteld bericht onderschept:
```
Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.
```

Je moet de juiste Caesar cipher shift-waarde (0-25) vinden om het te ontcijferen.

### Stap-voor-stap

1. **Start de challenge container:**
```bash
docker run -it caesar-cipher-challenge:latest
```

2. **Probeer verschillende shift-waarden** totdat het bericht duidelijk wordt

3. **De juiste antwoord:** Shift `3`

4. **Je krijgt de flag:**
```
FLAG: CTF{c43s4r_c1ph3r_m4st3r}
```

5. **Dien in op CTFd:**
   - Ga naar http://localhost:8000
   - Klik op "Caesar Cipher" challenge
   - Voer de flag in
   - Submit!

## 📁 Bestanden

```
.
├── caesar_challenge.py           # Interactieve Python challenge
├── Dockerfile.caesar             # Container image voor de challenge
├── docker-compose.yml            # Compose file voor beide services
├── add_ctf_challenge.py          # Script om challenge toe te voegen aan CTFd
├── fix_challenge.py              # Fix script voor flag type
├── .gitignore                    # Git ignore rules
└── README.md                     # Dit bestand
```

## 🔧 CTFd Setup

Bij eerste keer opstarten:

1. Open http://localhost:8000
2. Voltooi de setup wizard
3. Maak een admin account
4. De Caesar Cipher challenge verschijnt automatisch

## 🐳 Docker Commands

```bash
# Containers starten
docker compose up -d

# Containers stoppen
docker compose down

# Logs bekijken
docker compose logs -f

# Challenge container interactief uitvoeren
docker run -it caesar-cipher-challenge:latest

# CTFd logs bekijken
docker logs ctfd
```

## 🛠️ Troubleshooting

**Challenge verschijnt niet in CTFd?**
```bash
docker cp add_ctf_challenge.py ctfd:/tmp/
docker exec ctfd python /tmp/add_ctf_challenge.py
```

**Kan niet inloggen op CTFd?**
- Zorg dat je de setup wizard hebt voltooid
- Refresh de pagina (Ctrl+F5)

**Docker daemon is niet actief?**
- Start Docker Desktop of de Docker daemon

## 📝 Challenge Details

| Property | Waarde |
|----------|--------|
| Naam | Caesar Cipher |
| Categorie | Cryptography |
| Punten | 100 |
| Moeilijkheid | Easy |
| Flag | `CTF{c43s4r_c1ph3r_m4st3r}` |

## 🎓 Wat je leert

- Caesar cipher cryptografie
- Docker containers bouwen en uitvoeren
- Docker Compose voor multi-container setups
- CTFd platform gebruiken
- Flag submission workflow

## 📚 Meer Challenges Toevoegen

1. Maak een nieuwe Python script voor je challenge
2. Schrijf een Dockerfile
3. Voeg service toe aan docker-compose.yml
4. Registreer in CTFd via `add_ctf_challenge.py`

## 📄 Licentie

MIT

## 👨‍💻 Auteur

Gemaakt met Docker

---

**Veel succes met je CTF!** 🚩
