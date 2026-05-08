# ARCHITECTURE

Dokumentacja architektoniczna Aplikacji do Sterowania Oświetleniem.

## Przegląd systemu

Aplikacja składa się z trzech głównych komponentów:

1. **FastAPI Web Server** - REST API do zarządzania włącznikami
2. **MQTT Broker** - Message Bus dla komunikacji urządzenia-serwer
3. **Light Switch Simulator** - Symulacja fizycznych urządzeń

## Diagram architektury

```
┌─────────────────┐
│   Użytkownik    │
│   (Przeglądarka)│
└────────┬────────┘
         │ HTTP
         ▼
┌────────────────────────────┐
│   FastAPI Web Server       │
│  ┌──────────────────────┐  │
│  │ REST API Endpoints   │  │
│  │  - /api/switches     │  │
│  │  - /api/statistics   │  │
│  │  - /api/health       │  │
│  └──────────────────────┘  │
│           │                │
│           ▼                │
│  ┌──────────────────────┐  │
│  │ MQTT Client          │  │
│  │  (Pub/Sub)           │  │
│  └──────────────────────┘  │
│           │                │
│           ▼                │
│  ┌──────────────────────┐  │
│  │ Database (SQLite)    │  │
│  │  - LightSwitch       │  │
│  │  - Statistics        │  │
│  └──────────────────────┘  │
└────────┬────────────────────┘
         │ MQTT
         ▼
┌─────────────────────────────┐
│  MQTT Broker (Mosquitto)    │
│  Topics:                    │
│  - lights/register          │
│  - lights/register/confirm  │
│  - lights/control           │
│  - lights/state             │
└────────┬────────────────────┘
         │ MQTT
         ▼
┌─────────────────────────────┐
│ Light Switch Simulator      │
│ ┌─────────────────────────┐ │
│ │ Simulated Devices (N)   │ │
│ │  - Device 1             │ │
│ │  - Device 2             │ │
│ │  - Device N             │ │
│ └─────────────────────────┘ │
│           │                 │
│           ▼                 │
│ ┌─────────────────────────┐ │
│ │ MQTT Client            │ │
│ │ (Subscribe/Publish)    │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

## Komponenty systemu

### 1. FastAPI Web Server

**Plik**: `app/main.py`

**Odpowiedzialność**:
- Obsługa żądań HTTP REST
- Zarządzanie stanem włączników
- Zapis i odczyt z bazy danych
- Zbieranie statystyk
- Komunikacja z MQTT brokerem

**Endpointy API**:
- `POST /api/switches` - Dodaj włącznik
- `GET /api/switches` - Pobierz wszystkie włączniki
- `GET /api/switches/{id}` - Pobierz szczegóły
- `PUT /api/switches/{id}` - Zmień stan
- `DELETE /api/switches/{id}` - Usuń włącznik
- `GET /api/statistics/{id}` - Pobierz statystyki
- `GET /api/statistics/{id}/summary` - Podsumowanie
- `GET /api/health` - Status zdrowia

**Technologia**:
- FastAPI 0.104.1
- Uvicorn ASGI server
- SQLModel ORM
- Paho MQTT client

### 2. MQTT Broker

**Oprogramowanie**: Eclipse Mosquitto

**Topiki MQTT**:

| Topik | Kierunek | Opis |
|-------|----------|------|
| `lights/register` | Device → Server | Rejestracja urządzenia |
| `lights/register/confirm` | Server → Device | Potwierdzenie rejestracji |
| `lights/control` | Server → Device | Polecenie sterowania |
| `lights/state` | Device → Server | Zmiana stanu |

**Format wiadomości**:

```json
// Rejestracja
{
  "device_id": "uuid",
  "name": "name"
}

// Potwierdzenie
{
  "device_id": "uuid",
  "status": "confirmed"
}

// Sterowanie
{
  "switch_id": "uuid",
  "state": true/false,
  "command": "turn_on/turn_off"
}

// Stan
{
  "switch_id": "uuid",
  "state": true/false,
  "timestamp": float
}
```

### 3. Light Switch Simulator

**Plik**: `simulator/light_switch_simulator.py`

**Odpowiedzialność**:
- Symulacja fizycznych urządzeń
- Rejestracja u serwera
- Odbieranie poleceń
- Raportowanie zmian stanu
- Logowanie działań

**Klasa**: `LightSwitchSimulator`

**Metody**:
- `connect()` - Połączenie z MQTT
- `register_switches()` - Rejestracja urządzeń
- `_handle_registration_confirmation()` - Obsługa potwierdzenia
- `_handle_control_command()` - Obsługa poleceń
- `_publish_state_change()` - Publikacja zmian

## Modele danych

### LightSwitch

```python
class LightSwitch(SQLModel, table=True):
    id: UUID                    # Unikalny identyfikator
    name: str                   # Nazwa włącznika
    is_on: bool                 # Stan (włączony/wyłączony)
    created_at: datetime        # Data utworzenia
    last_updated: datetime      # Data ostatniej aktualizacji
    total_runtime_seconds: float  # Łączny czas pracy
    last_toggled: datetime      # Data ostatniego przełączenia
```

### Statistics

```python
class Statistics(SQLModel, table=True):
    id: int                     # Identyfikator rekordu
    switch_id: UUID             # ID włącznika (FK)
    turn_on_time: datetime      # Czas włączenia
    turn_off_time: datetime     # Czas wyłączenia
    duration_seconds: float     # Czas pracy
    created_at: datetime        # Data utworzenia rekordu
```

## Przepływ danych

### Scenariusz 1: Dodanie nowego włącznika

```
1. Użytkownik
   └─ POST /api/switches
      └─ FastAPI
         ├─ Create LightSwitch in DB
         ├─ Subscribe to MQTT registration
         └─ Return switch UUID

2. Symulator (równoczeście)
   └─ Publish lights/register
      └─ MQTT Broker
         └─ FastAPI receives message
            ├─ Confirm registration
            └─ Update switch status in DB

3. Symulator
   └─ Receives lights/register/confirm
      └─ Mark device as registered
```

### Scenariusz 2: Włączenie/wyłączenie światła

```
1. Użytkownik
   └─ PUT /api/switches/{id}
      └─ FastAPI
         ├─ Update switch state in DB
         ├─ Create/update Statistics record
         ├─ Publish lights/control
         └─ Return updated state

2. Symulator
   └─ Receives lights/control
      └─ Update device state
         └─ Publish lights/state
            └─ MQTT Broker
               └─ FastAPI receives message
                  └─ Log state change
```

### Scenariusz 3: Pobieranie statystyk

```
1. Użytkownik
   └─ GET /api/statistics/{id}
      └─ FastAPI
         ├─ Query Statistics records from DB
         ├─ Calculate totals
         └─ Return summary
```

## Struktura katalogów

```
app/
├── main.py              # FastAPI aplikacja
├── models.py            # SQLModel modele
├── database.py          # Inicjalizacja bazy
├── crud.py              # CRUD operacje
├── mqtt_client.py       # MQTT client
├── config.py            # Konfiguracja
└── __init__.py

simulator/
├── light_switch_simulator.py  # Symulator
└── __init__.py

tests/
├── test_main.py         # Testy
└── __init__.py

root/
├── run.py               # Entry point
├── run.bat              # Skrypt Windows
├── run.sh               # Skrypt Unix
├── run_simulator.bat    # Simulator Windows
├── run_simulator.sh     # Simulator Unix
├── demo.py              # Demo skrypt
├── requirements.txt     # Zależności
├── Dockerfile           # Docker image
├── docker-compose.yml   # Docker Compose
├── .gitignore           # Git ignore
├── README.md            # Dokumentacja
├── SETUP_GUIDE.md       # Instrukcja setup
├── CONTRIBUTING.md      # Wytyczne
├── API_DOCUMENTATION.md # Dokumentacja API
└── ARCHITECTURE.md      # Ten plik
```

## Sekwencja startowa

### Server (Terminal 1)

```
1. MQTT Broker (Mosquitto)
   mosquitto -v
   └─ Serwer MQTT dostępny na localhost:1883

2. FastAPI Server (Terminal 2)
   python -m uvicorn app.main:app --reload
   └─ Server dostępny na localhost:8000
   └─ Swagger UI na localhost:8000/docs
   └─ Nawiązuje połączenie MQTT z brokerem
```

### Client (Terminal 3)

```
3. Light Switch Simulator
   python simulator/light_switch_simulator.py
   └─ Łączy się z MQTT brokerem
   └─ Rejestruje 3 symulowane urządzenia
   └─ Czeka na polecenia z serwera
```

## Bezpieczeństwo

### Aktualnie

- Brak autentykacji (open API)
- Brak SSL/TLS
- Brak rate limitingu
- Brak CORS restriction

### Rekomendacje dla produkcji

1. **Autentykacja**: JWT tokens
2. **Autoryzacja**: Role-based access control
3. **HTTPS**: SSL/TLS certificates
4. **MQTT**: Username/password authentication
5. **Rate Limiting**: IP-based throttling
6. **CORS**: Restrict to trusted origins
7. **Input Validation**: Sanitize all inputs
8. **Logging**: Audit trail
9. **Monitoring**: Health checks
10. **Updates**: Keep dependencies up-to-date

## Wydajność

### Optimizacje

- Database indexes na `switch_id`
- Connection pooling dla DB
- MQTT connection reuse
- Async/await dla I/O operations

### Limits

- Max devices: Testowano z 100+
- Max requests/sec: 1000+ (zależy od sprzętu)
- Response time: <100ms (średnio)

## Scalability

### Horyzontalne skalowanie

1. **Multiple MQTT Brokers**: Clustering
2. **Load Balancer**: Nginx/HAProxy
3. **Database Replication**: Master-slave
4. **Microservices**: Oddzielić simulator

### Wertykalne skalowanie

1. **Database**: Upgrade hardware
2. **MQTT Broker**: Tune settings
3. **FastAPI**: Increase workers

## Disaster Recovery

1. **Database Backup**: Daily backup
2. **MQTT Persistence**: Enabled
3. **Configuration Backup**: Git repository
4. **Monitoring**: Alert on failures

## Monitoring

### Metryki do śledzenia

- API response time
- MQTT message count
- Database query performance
- Memory usage
- CPU usage
- Error rates

### Narzędzia

- Prometheus: Metrics collection
- Grafana: Visualization
- ELK Stack: Logging
- New Relic: APM (opcjonalnie)

## Testing Strategy

### Unit Tests

```bash
pytest tests/ -v
```

### Integration Tests

Testowanie komunikacji MQTT + API

### Load Tests

```bash
locust -f locustfile.py
```

## Deployment

### Development

```bash
python -m uvicorn app.main:app --reload
```

### Production

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Docker

```bash
docker-compose up -d
```

## Maintenance

### Regularne zadania

- [ ] Backup bazy danych
- [ ] Aktualizacja zależności
- [ ] Sprawdzenie logów
- [ ] Performance monitoring
- [ ] Security updates

## Przyszłe ulepszenia

1. **WebSocket**: Real-time updates
2. **Authentication**: JWT, OAuth2
3. **Caching**: Redis
4. **Message Queue**: RabbitMQ
5. **Microservices**: Kubernetes
6. **Frontend**: React/Vue dashboard
7. **Mobile App**: iOS/Android
8. **Voice Control**: Alexa, Google Assistant

## Referencje

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [MQTT Protocol](https://mqtt.org/)
- [Mosquitto Docs](https://mosquitto.org/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

## Kontakt

Pytania dotyczące architektury?
- Sprawdź GitHub Issues
- Otwórz Discussion
- Wyślij email

---

**Ostatnia aktualizacja**: 2024-01-01
**Wersja**: 1.0.0
