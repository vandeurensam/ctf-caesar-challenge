# Environment Setup Guide

## Flags Opslaan als Environment Variables

Alle vlaggen worden nu opgeslagen als Docker environment variables en nooit in code.

## Setup Stappen

### 1. Clone the repository

```bash
git clone https://github.com/vandeurensam/ctf-caesar-challenge.git
cd ctf-caesar-challenge
```

### 2. Create .env file

**Option A: Use the provided .env.example**

```bash
cp .env.example .env
```

Dit bevat default vlaggen voor development.

**Option B: Set your own flags**

```bash
# Create .env file with custom flags
cat > .env << 'EOF'
CAESAR_FLAG=CTF{your_caesar_flag}
IMAGE_METADATA_FLAG=CTF{your_image_flag}
HTTP_HEADERS_FLAG=CTF{your_http_flag}
EOF
```

### 3. Important: Never commit .env to git

```bash
# Make sure .gitignore includes .env
# This is already configured, but double check:
cat .gitignore | grep ".env"
```

The `.env` file is in `.gitignore` so it won't be accidentally committed.

### 4. Start all services

```bash
docker compose up -d
```

Docker Compose will automatically load the flags from `.env` into the containers.

### 5. Verify flags are loaded

```bash
# Check Caesar challenge
docker run -it caesar-challenge

# Check Image Metadata challenge  
docker run -it image-challenge

# Check HTTP Headers challenge
docker logs http-challenge
```

## How It Works

### When using Docker Compose

```yaml
# docker-compose.yml
services:
  caesar-challenge:
    env_file: .env  # Loads .env automatically
```

### When running containers manually

**With env file:**
```bash
docker run --env-file .env caesar-challenge:latest
```

**With individual env vars:**
```bash
docker run -e CAESAR_FLAG="CTF{your_flag}" caesar-challenge:latest
```

### In Dockerfiles

```dockerfile
ENV CAESAR_FLAG=default_value

# But container env var overrides this
docker run -e CAESAR_FLAG=custom_value image:latest
```

## Security Best Practices

✅ **DO:**
- Store flags in `.env` file
- Add `.env` to `.gitignore`
- Use `.env.example` as template
- Share `.env.example` (without real flags)
- Use environment variables in code: `os.getenv('FLAG_NAME')`

❌ **DON'T:**
- Commit `.env` to git
- Hardcode flags in Python scripts
- Share `.env` file
- Log flags to stdout in production
- Store secrets in Dockerfiles

## For Different Environments

### Development (.env)
```
CAESAR_FLAG=CTF{dev_caesar}
IMAGE_METADATA_FLAG=CTF{dev_image}
HTTP_HEADERS_FLAG=CTF{dev_http}
```

### Production
Use Docker secrets or a secret management service:
```bash
# Docker Swarm
docker secret create caesar_flag -
docker secret create image_flag -
```

Or use environment variable services like:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

## Accessing Flags in Code

### Python

```python
import os

flag = os.getenv('CAESAR_FLAG', 'default_value')
```

### Bash

```bash
echo $CAESAR_FLAG
```

### JavaScript (Flask templates)

Flags should NOT be exposed to frontend. Only server-side access.

## Verification

```bash
# Verify environment variables are set
docker exec caesar-challenge env | grep FLAG

# Verify .env file is loaded
cat .env

# Make sure .env is ignored by git
git status
# Should NOT show .env in untracked files
```

## Troubleshooting

**Flags not loading?**
```bash
# Check if .env file exists
ls -la .env

# Check docker-compose.yml has env_file
grep -A 2 "env_file" docker-compose.yml

# Check environment inside container
docker exec caesar-challenge env | grep CAESAR_FLAG
```

**Permission denied?**
```bash
# Make sure .env is readable
chmod 600 .env

# Make sure docker can read it
ls -la .env
```

**Git accidentally committed .env?**
```bash
# Remove from git history
git rm --cached .env
git commit -m "Remove .env file"

# Or reset if not pushed
git reset HEAD~1 .env
```

---

**Remember:** `.env` is for LOCAL DEVELOPMENT only. For production, use proper secret management!
