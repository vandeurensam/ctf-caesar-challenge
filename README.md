# CTFd Caesar Cipher Challenge

Een volledige CTF (Capture The Flag) setup met CTFd en meerdere interactieve challenges.

## 📋 Beschikbare Challenges

### 1. 🔐 Caesar Cipher (Cryptography) - 100 pts
Een klassieke cryptografie challenge. Ontcijfer het versleutelde bericht door de juiste shift-waarde te vinden.

**Flag:** `CTF{c43s4r_c1ph3r_m4st3r}`

### 2. 🖼️ Image Metadata (Forensics) - 150 pts
Zoek een verborgen vlag in de EXIF metadata van een afbeelding. Leer hoe metadata in afbeeldingen wordt opgeslagen.

**Flag:** `CTF{3x1f_m3t4d4t4_5ecr3t}`

### 3. 🌐 HTTP Headers & Cookies (Web) - 100 pts
Vind de vlag die verborgen is in HTTP response headers en cookies. Gebruik browser DevTools of de beschikbare tools.

**Flag:** `CTF{http_h34d3r_s3cr3t}`

**Access:** http://localhost:5000

---

## 🚀 Quick Start

### Vereisten
- Docker en Docker Compose geïnstalleerd

### Optie 1: Docker Compose (Aanbevolen)

```bash
git clone https://github.com/vandeurensam/ctf-caesar-challenge.git
cd ctf-caesar-challenge
docker compose up -d
```

**Services:**
- CTFd: http://localhost:8000
- HTTP Headers Challenge: http://localhost:5000

### Optie 2: Handmatig

```bash
# Start CTFd
docker run -d --name ctfd -p 8000:8000 ctfd/ctfd

# Caesar Cipher Challenge
docker build -f Dockerfile.caesar -t caesar-challenge:latest .
docker run -it caesar-challenge:latest

# Image Metadata Challenge
docker build -f Dockerfile.image_metadata -t image-metadata-challenge:latest .
docker run -it image-metadata-challenge:latest

# HTTP Headers Challenge
docker build -f Dockerfile.http_headers -t http-headers-challenge:latest .
docker run -it -p 5000:5000 http-headers-challenge:latest
```

---

## 🎯 Challenges Oplossen

### Challenge 1: Caesar Cipher

```bash
docker run -it caesar-challenge:latest
```

**Stappen:**
1. Je ziet een versleuteld bericht
2. Probeer verschillende shift-waarden (0-25)
3. Voer `3` in voor de juiste oplossing
4. Flag wordt getoond
5. Dien in op CTFd

### Challenge 2: Image Metadata

```bash
docker run -it image-metadata-challenge:latest
```

**Stappen:**
1. Je krijgt het commando `help` en `exit`
2. Voer `help` in
3. Je krijgt de EXIF metadata van de afbeelding
4. Zoek naar het veld met de flag
5. Dien in op CTFd

**Tools die je kunt gebruiken:**
- `exiftool` (commando regel)
- Python met PIL/piexif
- Online EXIF viewers

### Challenge 3: HTTP Headers & Cookies

Open http://localhost:5000 in je browser

**Methode 1: Browser DevTools**
1. Druk F12
2. Ga naar Network tab
3. Refresh de pagina
4. Check Response Headers op verdachte entries
5. Zoek naar headers die beginnen met "X-"

**Methode 2: Gebruik de beschikbare buttons**
1. "Fetch Response Headers" - Zie alle headers
2. "Check Cookies" - Bekijk cookies
3. "Inspect Full Response" - Zie volledige data

---

## 📁 Bestanden Structuur

```
.
├── caesar_challenge.py              # Caesar cipher challenge
├── Dockerfile.caesar                # Caesar challenge container
├── image_metadata_challenge.py       # Image metadata challenge
├── Dockerfile.image_metadata        # Image metadata container
├── http_headers_challenge.py        # HTTP headers/cookies challenge
├── Dockerfile.http_headers          # HTTP challenge container
├── docker-compose.yml               # Alle services
├── add_all_challenges.py            # Add alle challenges aan CTFd
├── .gitignore                       # Git ignore rules
└── README.md                        # Dit bestand
```

---

## 🐳 Docker Commands

```bash
# Alles starten
docker compose up -d

# Alles stoppen
docker compose down

# Logs bekijken
docker compose logs -f

# Specifieke service logs
docker logs -f ctfd
docker logs -f http-challenge
docker logs -f image-challenge

# Challenges uitvoeren
docker run -it caesar-challenge:latest
docker run -it image-metadata-challenge:latest
docker run -it -p 5000:5000 http-headers-challenge:latest
```

---

## 🔧 CTFd Setup

Bij eerste keer opstarten:

1. Open http://localhost:8000
2. Voltooi de setup wizard
3. Maak een admin account
4. De challenges verschijnen automatisch

**Challenges handmatig toevoegen:**
```bash
docker cp add_all_challenges.py ctfd:/tmp/
docker exec ctfd python /tmp/add_all_challenges.py
```

---

## 🛠️ Troubleshooting

**Challenges verschijnen niet in CTFd?**
```bash
docker cp add_all_challenges.py ctfd:/tmp/
docker exec ctfd python /tmp/add_all_challenges.py
```

**HTTP Challenge port conflict?**
```bash
# Pas de port aan in docker-compose.yml
# Of voer uit met ander port:
docker run -d -p 5001:5000 http-headers-challenge:latest
```

**Docker daemon is niet actief?**
- Start Docker Desktop of de Docker daemon

**Kan niet clonen van GitHub?**
- Zorg dat je internet hebt
- Controleer SSH keys als je SSH gebruikt

---

## 📚 Learning Resources

### Caesar Cipher
- [Caesar Cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)

### EXIF Data
- [EXIF Data - Wikipedia](https://en.wikipedia.org/wiki/Exif)
- [ExifTool Documentation](https://exiftool.org/)
- [Image Forensics](https://en.wikipedia.org/wiki/Digital_forensics)

### HTTP Protocol
- [HTTP Headers - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [HTTP Cookies - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [Browser Developer Tools](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_are_browser_developer_tools)

---

## 📝 Challenge Details

| Challenge | Categorie | Punten | Moeilijkheid | Type |
|-----------|-----------|--------|-------------|------|
| Caesar Cipher | Cryptography | 100 | Easy | Klassiek |
| Image Metadata | Forensics | 150 | Easy-Medium | Forensisch |
| HTTP Headers & Cookies | Web | 100 | Easy | Web Security |
| **TOTAAL** | | **350** | | |

---

## 🎓 Wat je leert

- **Caesar Cipher**: Klassieke cryptografie, brute-force aanvallen
- **EXIF Metadata**: Digitale forensics, metadata analyse
- **HTTP Headers**: Web security, network protocols, DevTools

---

## 🚩 Score Tracking

Dien je flags in op CTFd via:
1. http://localhost:8000
2. Klik op "Challenges"
3. Klik op de challenge
4. Voer de flag in
5. Klik "Submit"

**Totaal mogelijk: 350 punten**

---

## 👨‍💻 Bijdragen

Wil je meer challenges toevoegen?

1. Maak een nieuwe Python script met je challenge
2. Schrijf een Dockerfile
3. Voeg service toe aan docker-compose.yml
4. Update add_all_challenges.py
5. Test alles

---

## 📄 Licentie

MIT

---

**Veel succes met je CTF!** 🚩

Voor vragen of problemen, check de troubleshooting sectie of create een issue op GitHub.
