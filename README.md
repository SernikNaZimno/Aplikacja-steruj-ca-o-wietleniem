<!-- dokumentacja projektu została napisana przez narzędzia do generowania kodu. -->

# Aplikacja do Sterowania Oświetleniem

Aplikacja do symulowania komunikacji systemu zarządzania oświetleniem za pośrednictwem MQTT. Projekt składa się z dwóch głównych komponów:
1. **FastAPI Web Application** - zarządzanie włącznikami światła i statystykami
2. **MQTT Light Switch Simulator** - symulacja fizycznych włączników światła

## Architektura Projektu

### 1. Aplikacja FastAPI (`app/`)

Serwer webowy odpowiedzialny za:
- Zarządzanie włącznikami światła (dodawanie, usuwanie, włączanie/wyłączanie)
- Przechowywanie stanu włączników w bazie danych
- Zbieranie i analizowanie statystyk czasu działania oświetlenia
- Komunikacja z urządzeniami poprzez MQTT

**Pliki:**
- `main.py` - Główna aplikacja FastAPI z definicją endpointów API
- `models.py` - Modele bazy danych (SQLModel) i schematy Pydantic
- `database.py` - Inicjalizacja bazy danych i zarządzanie sesjami
- `crud.py` - Operacje na bazie danych (Create, Read, Update, Delete)
- `mqtt_client.py` - Klient MQTT do komunikacji z urządzeniami
- `config.py` - Konfiguracja aplikacji (MQTT, baza danych, itd.)

### 2. Symulator MQTT (`simulator/`)

Aplikacja symulująca fizyczne włączniki światła:
- Rejestracja urządzeń u serwera
- Odbieranie poleceń włączenia/wyłączenia z serwera
- Symulacja zmian stanu oświetlenia
- Wysyłanie informacji o zmianach stanu

**Pliki:**
- `light_switch_simulator.py` - Główny symulator obsługujący wiele urządzeń

## Wymagania

- Python 3.8+
- MQTT Broker (np. Mosquitto)
- SQLite (domyślna baza danych)

## Instalacja

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/SernikNaZimno/Aplikacja-steruj-ca-o-wietleniem.git
cd Aplikacja-steruj-ca-o-wietleniem
```

### 2. Utworzenie wirtualnego środowiska

```bash
# Na Windows
python -m venv venv
venv\Scripts\activate

# Na macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Konfiguracja MQTT Broker'a

Zainstaluj i uruchom MQTT Broker (np. Mosquitto):

**Windows (z Chocolatey):**
```bash
choco install mosquitto
```

**macOS (z Homebrew):**
```bash
brew install mosquitto
brew services start mosquitto
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

## Uruchamianie Aplikacji

### 1. Uruchamianie serwera FastAPI

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Serwer będzie dostępny pod adresem: `http://localhost:8000`

Dokumentacja API Swagger: `http://localhost:8000/docs`

### 2. Uruchamianie symulatora

W nowym terminalu:

```bash
python simulator/light_switch_simulator.py
```

## Dokumentacja API

### Endpointy Włączników

#### Dodanie nowego włącznika
```
POST /api/switches
Content-Type: application/json

{
  "name": "Lampa w kuchni"
}

Response 200:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Lampa w kuchni",
  "is_on": false,
  "created_at": "2024-01-01T10:00:00",
  "last_updated": "2024-01-01T10:00:00",
  "total_runtime_seconds": 0.0,
  "last_toggled": null
}
```

#### Pobranie wszystkich włączników
```
GET /api/switches

Response 200:
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Lampa w kuchni",
    "is_on": false,
    ...
  }
]
```

#### Pobranie szczegółów włącznika
```
GET /api/switches/{switch_id}

Response 200:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Lampa w kuchni",
  "is_on": false,
  ...
}
```

#### Włączenie/wyłączenie światła
```
PUT /api/switches/{switch_id}
Content-Type: application/json

{
  "is_on": true
}

Response 200:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Lampa w kuchni",
  "is_on": true,
  "last_updated": "2024-01-01T10:05:00",
  ...
}
```

#### Usunięcie włącznika
```
DELETE /api/switches/{switch_id}

Response 200:
{
  "status": "success",
  "message": "Light switch deleted"
}
```

### Endpointy Statystyk

#### Pobranie statystyk dla włącznika
```
GET /api/statistics/{switch_id}

Response 200:
[
  {
    "id": 1,
    "switch_id": "550e8400-e29b-41d4-a716-446655440000",
    "turn_on_time": "2024-01-01T10:00:00",
    "turn_off_time": "2024-01-01T10:05:00",
    "duration_seconds": 300.0,
    "created_at": "2024-01-01T10:00:00"
  }
]
```

#### Pobranie streszczenia statystyk
```
GET /api/statistics/{switch_id}/summary

Response 200:
{
  "switch_id": "550e8400-e29b-41d4-a716-446655440000",
  "switch_name": "Lampa w kuchni",
  "total_runtime_seconds": 1200.0,
  "total_cycles": 4,
  "average_runtime_seconds": 300.0
}
```

#### Sprawdzenie zdrowia aplikacji
```
GET /api/health

Response 200:
{
  "status": "healthy",
  "mqtt_connected": true
}
```

## Topiki MQTT

Aplikacja używa następujących topików MQTT:

| Topik | Kierunek | Opis |
|-------|----------|------|
| `lights/register` | Urządzenie → Serwer | Rejestracja nowego urządzenia |
| `lights/register/confirm` | Serwer → Urządzenie | Potwierdzenie rejestracji |
| `lights/control` | Serwer → Urządzenie | Polecenie włączenia/wyłączenia |
| `lights/state` | Urządzenie → Serwer | Zmiana stanu światła |

### Formaty wiadomości MQTT

**Rejestracja urządzenia:**
```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Lampa w kuchni"
}
```

**Potwierdzenie rejestracji:**
```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "confirmed"
}
```

**Polecenie sterowania:**
```json
{
  "switch_id": "550e8400-e29b-41d4-a716-446655440000",
  "state": true,
  "command": "turn_on"
}
```

**Zmiana stanu:**
```json
{
  "switch_id": "550e8400-e29b-41d4-a716-446655440000",
  "state": true,
  "timestamp": 1704110400.0
}
```

## Testowanie

### Uruchomienie testów jednostkowych

```bash
pytest tests/ -v
```

### Testowanie API za pomocą curl

```bash
# Dodanie nowego włącznika
curl -X POST http://localhost:8000/api/switches \
  -H "Content-Type: application/json" \
  -d '{"name": "Lampa testowa"}'

# Pobranie wszystkich włączników
curl http://localhost:8000/api/switches

# Włączenie światła
curl -X PUT http://localhost:8000/api/switches/{switch_id} \
  -H "Content-Type: application/json" \
  -d '{"is_on": true}'

# Pobranie statystyk
curl http://localhost:8000/api/statistics/{switch_id}/summary

# Sprawdzenie zdrowia
curl http://localhost:8000/api/health
```

### Testowanie MQTT

Możesz używać `mosquitto_sub` i `mosquitto_pub`:

```bash
# Subskrybuj topik rejestracji
mosquitto_sub -t "lights/register"

# Publikuj wiadomość rejestracji
mosquitto_pub -t "lights/register" -m '{"device_id":"test123","name":"Test Light"}'
```

## Struktura Projektu

```
Aplikacja-steruj-ca-o-wietleniem/
├── app/
│   ├── __init__.py
│   ├── main.py              # Główna aplikacja FastAPI
│   ├── models.py            # Modele bazy danych
│   ├── database.py          # Inicjalizacja bazy danych
│   ├── crud.py              # Operacje na bazie danych
│   ├── mqtt_client.py       # Klient MQTT
│   └── config.py            # Konfiguracja
├── simulator/
│   ├── __init__.py
│   └── light_switch_simulator.py  # Symulator urządzeń
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Testy jednostkowe
├── .gitignore
├── requirements.txt         # Zależności Python
└── README.md               # Dokumentacja
```

## Zmienne Środowiskowe

Możesz skonfigurować aplikację za pomocą zmiennych środowiskowych:

```bash
# MQTT
export MQTT_BROKER_HOST=localhost
export MQTT_BROKER_PORT=1883
export MQTT_CLIENT_ID=fastapi-app

# Baza danych
export DATABASE_URL=sqlite:///./test.db

# FastAPI
export DEBUG=True
```

## Wdrażanie

Projekt może być wdrażany przy użyciu Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Git Historia

Projekt zawiera historię Git z regularnymi commitami:

```bash
git log --oneline
```

Opis branchy i commitów:
- `main` - Gałąź główna z gotowym kodem
- Poszczególne commity opisują dodawane funkcjonalności

## Autorzy

- Adam Henke

## Licencja

Projekt jest licencjonowany na licencji MIT.

## Problemy i Wsparcie

Jeśli napotkasz problem:

1. Sprawdź czy MQTT Broker jest uruchomiony
2. Sprawdź logi aplikacji
3. Upewnij się że wszystkie zależności są zainstalowane
4. Sprawdź połączenie sieciowe

## Przyszłe Ulepszenia

- [ ] Dodanie uwierzytelniania do API
- [ ] Persystencja zmian stanu na dysku
- [ ] Zaawansowane harmonogramy automatyzacji
- [ ] Interfejs webowy do zarządzania urządzeniami
- [ ] Powiadomienia o zmianach stanu
- [ ] Obsługa różnych typów urządzeń
- [ ] Integracja z asystentami głosowymi

## Ocena Projektowa

Projekt jest oceniany w następujących kategoriach:

- **Styl i Git (2 punkty)**: Czysty kod, regularne commity, organizacja repozytorium
- **FastAPI (5 punktów)**: Poprawna architektura, obsługa MQTT, zarządzanie stanem
- **Symulator (5 punktów)**: Poprawna symulacja urządzeń, obsługa poleceń
- **MQTT (3 punkty)**: Poprawna komunikacja, obsługa topików, niezawodność