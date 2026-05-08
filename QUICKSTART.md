# QUICK START

Szybki start - uruchom aplikację w 3 krokach!

## 📋 Wymagania

- Python 3.8+
- MQTT Broker (Mosquitto)
- Terminal/PowerShell

## ⚡ Szybki Start (3 kroki)

### Krok 1: Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/SernikNaZimno/Aplikacja-steruj-ca-o-wietleniem.git
cd Aplikacja-steruj-ca-o-wietleniem

# Zainstaluj zależności
pip install -r requirements.txt
```

### Krok 2: Uruchomienie

**Terminal 1 - MQTT Broker:**
```bash
mosquitto -v
```

**Terminal 2 - FastAPI Server:**
```bash
python -m uvicorn app.main:app --reload
```

**Terminal 3 - Symulator:**
```bash
python simulator/light_switch_simulator.py
```

### Krok 3: Testowanie

Otwórz w przeglądarce:
```
http://localhost:8000/docs
```

## 🎯 Pierwsze Kroki

### 1. Sprawdź status API
```bash
curl http://localhost:8000/api/health
```

### 2. Dodaj włącznik
```bash
curl -X POST http://localhost:8000/api/switches \
  -H "Content-Type: application/json" \
  -d '{"name": "My Light"}'
```

### 3. Włącz światło
```bash
curl -X PUT http://localhost:8000/api/switches/YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{"is_on": true}'
```

## 🐳 Docker Quick Start

```bash
# Uruchomienie z Docker Compose
docker-compose up -d

# Sprawdzenie logów
docker-compose logs -f
```

## 📖 Dokumentacja

- **Setup**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **API**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Architektura**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔗 Linki

- 🌐 API: http://localhost:8000
- 📚 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc

## ⚙️ Skrypty

### Windows
```bash
run.bat              # Uruchom serwer
run_simulator.bat    # Uruchom symulator
```

### macOS/Linux
```bash
./run.sh             # Uruchom serwer
./run_simulator.sh   # Uruchom symulator
```

## 🆘 Problemy?

### Port już w użyciu?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### MQTT nie dostępny?
```bash
# Sprawdź czy Mosquitto jest uruchomiony
mosquitto -v
```

### Brak modułów?
```bash
pip install -r requirements.txt
```

## 💡 Przydatne Komendy

```bash
# Uruchom testy
pytest tests/ -v

# Uruchom demo
python demo.py

# Sprawdź MQTT
mosquitto_sub -t "lights/#"

# Format kodu
black app/ simulator/

# Lint
pylint app/
```

## 🎮 Testuj API

### Swagger UI (Rekomendowany)
```
http://localhost:8000/docs
```

### cURL
```bash
# Lista włączników
curl http://localhost:8000/api/switches

# Statystyki
curl http://localhost:8000/api/statistics/{id}/summary
```

### Python
```python
import requests

r = requests.get('http://localhost:8000/api/switches')
print(r.json())
```

## 📊 Status

```bash
# Sprawdź zdrowość
curl http://localhost:8000/api/health
```

## 🚀 Następne kroki

1. Przeczytaj [README.md](README.md)
2. Zapoznaj się z [ARCHITECTURE.md](ARCHITECTURE.md)
3. Eksperymentuj z API
4. Czytaj [CONTRIBUTING.md](CONTRIBUTING.md) jeśli chcesz kontrybuować

## 📞 Pomoc

- 📖 Dokumentacja: Czytaj plik .md
- 🐛 Issues: Sprawdź GitHub Issues
- 💬 Dyskusje: GitHub Discussions
- 🎓 API Docs: http://localhost:8000/docs

---

**Powodzenia!** 🎉

Jeśli masz jakieś pytania, sprawdź dokumentację lub otwórz issue.
