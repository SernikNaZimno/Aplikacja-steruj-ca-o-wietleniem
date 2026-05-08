# SETUP GUIDE - Aplikacja do Sterowania Oświetleniem

Przewodnik krok po kroku do uruchomienia aplikacji do sterowania oświetleniem.

## Wymagania systemowe

- **Python**: 3.8 lub wyżej
- **MQTT Broker**: Mosquitto (lub kompatybilny broker)
- **System operacyjny**: Windows, macOS lub Linux
- **RAM**: Minimum 512 MB
- **Miejsce na dysku**: 500 MB

## Kroki instalacji

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/SernikNaZimno/Aplikacja-steruj-ca-o-wietleniem.git
cd Aplikacja-steruj-ca-o-wietleniem
```

### 2. Konfiguracja MQTT Broker'a

#### Windows z Chocolatey

```bash
# Instalacja Mosquitto
choco install mosquitto

# Uruchomienie Mosquitto
mosquitto -v
```

#### macOS z Homebrew

```bash
# Instalacja Mosquitto
brew install mosquitto

# Uruchomienie (w tle)
brew services start mosquitto

# Sprawdzenie statusu
brew services list
```

#### Linux (Ubuntu/Debian)

```bash
# Instalacja
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients

# Uruchomienie
sudo systemctl start mosquitto

# Sprawdzenie statusu
sudo systemctl status mosquitto

# Włączenie przy starcie systemu
sudo systemctl enable mosquitto
```

#### Docker

```bash
# Uruchomienie Mosquitto w Docker
docker run -d \
  -p 1883:1883 \
  -p 9001:9001 \
  --name mosquitto \
  eclipse-mosquitto:2.0
```

### 3. Konfiguracja Python

#### Opcja A: Automatyczne (Recommended)

**Na Windows:**
```bash
run.bat
```

**Na macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

#### Opcja B: Manualna

```bash
# Utworzenie wirtualnego środowiska
python -m venv venv

# Aktywacja (Windows)
venv\Scripts\activate.bat

# Aktywacja (macOS/Linux)
source venv/bin/activate

# Instalacja zależności
pip install -r requirements.txt

# Uruchomienie aplikacji
python -m uvicorn app.main:app --reload
```

### 4. Konfiguracja zmiennych środowiskowych (opcjonalne)

Stwórz plik `.env` w głównym katalogu:

```env
# MQTT Configuration
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID=fastapi-app

# Database
DATABASE_URL=sqlite:///./test.db

# Application
DEBUG=True
```

## Uruchomienie aplikacji

### Terminal 1: MQTT Broker

```bash
# Upewnij się, że Mosquitto jest uruchomiony
mosquitto -v
```

### Terminal 2: FastAPI Serwer

```bash
# Aktywuj wirtualne środowisko (jeśli nie jest aktywne)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

# Uruchom serwer
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# LUB użyj skryptu
python run.py
```

Serwer będzie dostępny na: **http://localhost:8000**

### Terminal 3: MQTT Light Switch Simulator

```bash
# Aktywuj wirtualne środowisko (jeśli nie jest aktywne)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

# Uruchom symulator
python simulator/light_switch_simulator.py

# LUB użyj skryptu
./run_simulator.sh    # macOS/Linux
run_simulator.bat     # Windows
```

## Weryfikacja instalacji

### 1. Sprawdzenie zdrowia API

```bash
curl http://localhost:8000/api/health
```

Oczekiwana odpowiedź:
```json
{
  "status": "healthy",
  "mqtt_connected": true
}
```

### 2. Dostęp do dokumentacji API

Otwórz w przeglądarce: **http://localhost:8000/docs**

Tutaj możesz testować wszystkie endpointy.

### 3. Uruchomienie demo

```bash
# Aktywuj wirtualne środowisko
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

# Uruchom demo
python demo.py
```

## Testowanie

### Testy jednostkowe

```bash
# Aktywuj wirtualne środowisko
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

# Uruchom testy
pytest tests/ -v

# Testy z pokryciem kodu
pytest tests/ --cov=app --cov-report=html
```

### Testowanie ręczne z curl

```bash
# Dodaj nowy włącznik
curl -X POST http://localhost:8000/api/switches \
  -H "Content-Type: application/json" \
  -d '{"name": "Kitchen Light"}'

# Pobierz wszystkie włączniki
curl http://localhost:8000/api/switches

# Włącz światło (zamień UUID na rzeczywisty)
curl -X PUT http://localhost:8000/api/switches/YOUR_SWITCH_ID \
  -H "Content-Type: application/json" \
  -d '{"is_on": true}'
```

## Docker

### Budowanie image

```bash
docker build -t lighting-control .
```

### Uruchomienie z Docker Compose

```bash
docker-compose up -d
```

### Sprawdzenie logów

```bash
docker-compose logs -f fastapi-app
```

## Rozwiązywanie problemów

### Problem: "Connection refused" (MQTT)

**Przyczyna**: MQTT Broker nie jest uruchomiony.

**Rozwiązanie**:
```bash
mosquitto -v
```

### Problem: "Port 8000 already in use"

**Przyczyna**: Inny proces zajmuje port 8000.

**Rozwiązanie - Windows**:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Rozwiązanie - macOS/Linux**:
```bash
lsof -i :8000
kill -9 <PID>
```

### Problem: "ImportError: No module named 'sqlmodel'"

**Przyczyna**: Zależności nie są zainstalowane.

**Rozwiązanie**:
```bash
pip install -r requirements.txt
```

### Problem: Symulator nie rejestruje urządzeń

**Sprawdzenie**:
1. Czy MQTT Broker jest uruchomiony?
2. Czy FastAPI server jest uruchomiony?
3. Sprawdź logi obu aplikacji pod kątem błędów

## Struktura katalogu po instalacji

```
Aplikacja-steruj-ca-o-wietleniem/
├── app/                    # Główna aplikacja FastAPI
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── mqtt_client.py
│   ├── config.py
│   └── __init__.py
├── simulator/              # Symulator urządzeń MQTT
│   ├── light_switch_simulator.py
│   └── __init__.py
├── tests/                  # Testy
│   ├── test_main.py
│   └── __init__.py
├── venv/                   # Wirtualne środowisko (utworzone)
├── test.db                 # Baza danych SQLite (utworzona)
├── .gitignore
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md          # Ten plik
├── Dockerfile
├── docker-compose.yml
├── run.py
├── run.sh
├── run.bat
├── run_simulator.sh
├── run_simulator.bat
├── demo.py
└── .env                    # (opcjonalnie)
```

## Następne kroki

1. **Zapoznaj się z dokumentacją API**: http://localhost:8000/docs
2. **Uruchom demo**: `python demo.py`
3. **Przeczytaj README.md** dla pełnej dokumentacji
4. **Eksperimentuj z API** za pomocą Swagger UI

## Przydatne komendy

```bash
# Sprawdzenie wersji Python
python --version

# Sprawdzenie wersji pip
pip --version

# Sprawdzenie zainstalowanych pakietów
pip list

# Sprawdzenie, czy port jest w użyciu
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Uruchomienie tylko Mosquitto
mosquitto -v

# Test MQTT
mosquitto_pub -t "test/topic" -m "Hello World"
mosquitto_sub -t "test/topic"

# Wyświetlenie logów Docker
docker-compose logs -f

# Wyczyszczenie bazy danych
rm test.db
```

## Wsparcie

Jeśli napotkasz problem:
1. Sprawdź sekcję "Rozwiązywanie problemów"
2. Przeanalizuj logi aplikacji
3. Sprawdź GitHub Issues
4. Sprawdź dokumentację zależności

## Zasoby

- [FastAPI Dokumentacja](https://fastapi.tiangolo.com/)
- [MQTT Dokumentacja](https://mqtt.org/)
- [SQLModel Dokumentacja](https://sqlmodel.tiangolo.com/)
- [Mosquitto Dokumentacja](https://mosquitto.org/)

## Powodzenia!

Aplikacja jest teraz gotowa do użytku. Miłej zabawy!
