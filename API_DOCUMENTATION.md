# API DOCUMENTATION

Kompletna dokumentacja REST API dla Aplikacji do Sterowania Oświetleniem.

## Base URL

```
http://localhost:8000/api
```

## Autentykacja

Aktualnie API nie wymaga autentykacji. Przyszłe wersje będą zawierać JWT lub API keys.

## Format odpowiedzi

Wszystkie odpowiedzi są w formacie JSON.

### Sukces (2xx)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Kitchen Light",
  "is_on": true,
  "created_at": "2024-01-01T10:00:00",
  "last_updated": "2024-01-01T10:05:00",
  "total_runtime_seconds": 300.0,
  "last_toggled": "2024-01-01T10:05:00"
}
```

### Błąd (4xx, 5xx)

```json
{
  "detail": "Light switch not found"
}
```

## Kody błędów

| Kod | Opis |
|-----|------|
| 200 | OK - Żądanie powiodło się |
| 201 | Created - Zasób został utworzony |
| 400 | Bad Request - Błędny format żądania |
| 404 | Not Found - Zasób nie został znaleziony |
| 500 | Internal Server Error - Błąd serwera |

## Endpointy

### Light Switches

#### POST /switches

Dodaj nowy włącznik światła.

**Request:**
```bash
curl -X POST http://localhost:8000/api/switches \
  -H "Content-Type: application/json" \
  -d '{"name": "Kitchen Light"}'
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Kitchen Light",
  "is_on": false,
  "created_at": "2024-01-01T10:00:00",
  "last_updated": "2024-01-01T10:00:00",
  "total_runtime_seconds": 0.0,
  "last_toggled": null
}
```

#### GET /switches

Pobierz wszystkie włączniki.

**Request:**
```bash
curl http://localhost:8000/api/switches
```

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Kitchen Light",
    "is_on": false,
    "created_at": "2024-01-01T10:00:00",
    "last_updated": "2024-01-01T10:00:00",
    "total_runtime_seconds": 0.0,
    "last_toggled": null
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Bedroom Light",
    "is_on": true,
    "created_at": "2024-01-01T10:05:00",
    "last_updated": "2024-01-01T10:05:00",
    "total_runtime_seconds": 300.0,
    "last_toggled": "2024-01-01T10:05:00"
  }
]
```

#### GET /switches/{switch_id}

Pobierz szczegóły konkretnego włącznika.

**Parameters:**
- `switch_id` (UUID) - ID włącznika

**Request:**
```bash
curl http://localhost:8000/api/switches/550e8400-e29b-41d4-a716-446655440000
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Kitchen Light",
  "is_on": false,
  "created_at": "2024-01-01T10:00:00",
  "last_updated": "2024-01-01T10:00:00",
  "total_runtime_seconds": 0.0,
  "last_toggled": null
}
```

**Response (404):**
```json
{
  "detail": "Light switch not found"
}
```

#### PUT /switches/{switch_id}

Zmień stan włącznika.

**Parameters:**
- `switch_id` (UUID) - ID włącznika

**Request Body:**
```json
{
  "is_on": true
}
```

**Request:**
```bash
curl -X PUT http://localhost:8000/api/switches/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"is_on": true}'
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Kitchen Light",
  "is_on": true,
  "created_at": "2024-01-01T10:00:00",
  "last_updated": "2024-01-01T10:05:30",
  "total_runtime_seconds": 0.0,
  "last_toggled": "2024-01-01T10:05:30"
}
```

#### DELETE /switches/{switch_id}

Usuń włącznik.

**Parameters:**
- `switch_id` (UUID) - ID włącznika

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/switches/550e8400-e29b-41d4-a716-446655440000
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Light switch deleted"
}
```

**Response (404):**
```json
{
  "detail": "Light switch not found"
}
```

### Statistics

#### GET /statistics/{switch_id}

Pobierz wszystkie rekordy statystyk dla włącznika.

**Parameters:**
- `switch_id` (UUID) - ID włącznika

**Request:**
```bash
curl http://localhost:8000/api/statistics/550e8400-e29b-41d4-a716-446655440000
```

**Response (200):**
```json
[
  {
    "id": 1,
    "switch_id": "550e8400-e29b-41d4-a716-446655440000",
    "turn_on_time": "2024-01-01T10:00:00",
    "turn_off_time": "2024-01-01T10:05:00",
    "duration_seconds": 300.0,
    "created_at": "2024-01-01T10:00:00"
  },
  {
    "id": 2,
    "switch_id": "550e8400-e29b-41d4-a716-446655440000",
    "turn_on_time": "2024-01-01T10:10:00",
    "turn_off_time": "2024-01-01T10:15:00",
    "duration_seconds": 300.0,
    "created_at": "2024-01-01T10:10:00"
  }
]
```

#### GET /statistics/{switch_id}/summary

Pobierz podsumowanie statystyk dla włącznika.

**Parameters:**
- `switch_id` (UUID) - ID włącznika

**Request:**
```bash
curl http://localhost:8000/api/statistics/550e8400-e29b-41d4-a716-446655440000/summary
```

**Response (200):**
```json
{
  "switch_id": "550e8400-e29b-41d4-a716-446655440000",
  "switch_name": "Kitchen Light",
  "total_runtime_seconds": 1200.0,
  "total_cycles": 4,
  "average_runtime_seconds": 300.0
}
```

### Health

#### GET /health

Sprawdź stan aplikacji i połączenia MQTT.

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "mqtt_connected": true
}
```

## Modele danych

### LightSwitch

```json
{
  "id": "UUID",
  "name": "string",
  "is_on": "boolean",
  "created_at": "datetime",
  "last_updated": "datetime",
  "total_runtime_seconds": "float",
  "last_toggled": "datetime (nullable)"
}
```

### Statistics

```json
{
  "id": "integer",
  "switch_id": "UUID",
  "turn_on_time": "datetime",
  "turn_off_time": "datetime (nullable)",
  "duration_seconds": "float (nullable)",
  "created_at": "datetime"
}
```

### StatisticsSummary

```json
{
  "switch_id": "UUID",
  "switch_name": "string",
  "total_runtime_seconds": "float",
  "total_cycles": "integer",
  "average_runtime_seconds": "float (nullable)"
}
```

## Przykłady użycia

### Python (requests)

```python
import requests

# Dodaj włącznik
response = requests.post(
    "http://localhost:8000/api/switches",
    json={"name": "Kitchen Light"}
)
switch = response.json()
print(f"Created switch: {switch['id']}")

# Włącz światło
response = requests.put(
    f"http://localhost:8000/api/switches/{switch['id']}",
    json={"is_on": True}
)
print(f"Light is now: {'ON' if response.json()['is_on'] else 'OFF'}")

# Pobierz statystyki
response = requests.get(
    f"http://localhost:8000/api/statistics/{switch['id']}/summary"
)
stats = response.json()
print(f"Total runtime: {stats['total_runtime_seconds']}s")
```

### JavaScript (fetch)

```javascript
// Dodaj włącznik
const response = await fetch('http://localhost:8000/api/switches', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Kitchen Light' })
});
const switchData = await response.json();
console.log(`Created switch: ${switchData.id}`);

// Włącz światło
const toggleResponse = await fetch(
  `http://localhost:8000/api/switches/${switchData.id}`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_on: true })
  }
);
const updated = await toggleResponse.json();
console.log(`Light is now: ${updated.is_on ? 'ON' : 'OFF'}`);
```

### cURL

```bash
#!/bin/bash

# Dodaj włącznik
SWITCH=$(curl -s -X POST http://localhost:8000/api/switches \
  -H "Content-Type: application/json" \
  -d '{"name": "Kitchen Light"}')

SWITCH_ID=$(echo $SWITCH | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

echo "Created switch: $SWITCH_ID"

# Włącz światło
curl -X PUT http://localhost:8000/api/switches/$SWITCH_ID \
  -H "Content-Type: application/json" \
  -d '{"is_on": true}'

echo "Light turned ON"

# Pobierz statystyki
curl http://localhost:8000/api/statistics/$SWITCH_ID/summary
```

## Rate Limiting

Aktualnie brak limitów. Przyszłe wersje będą zawierać rate limiting.

## CORS

CORS jest aktualnie włączony dla wszystkich źródeł. W produkcji powinien być ograniczony.

## Versioning

API jest w wersji 1.0. Przyszłe zmiany będą zachować kompatybilność wstecz.

## Błędy

### Wspólne błędy

**400 Bad Request - Błędny format JSON**
```json
{
  "detail": "Invalid request body"
}
```

**404 Not Found - Zasób nie istnieje**
```json
{
  "detail": "Light switch not found"
}
```

**500 Internal Server Error - Błąd serwera**
```json
{
  "detail": "Internal server error"
}
```

## WebSocket (przyszłe)

Przyszłe wersje będą zawierać WebSocket doreal-time aktualizacji stanu.

## Changelog

### v1.0.0 (Aktualnie)

- Podstawowe operacje CRUD na włącznikach
- Statystyki czasu działania
- Integracja MQTT
- Dokumentacja API
