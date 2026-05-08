# CONTRIBUTING

Dziękujemy za zainteresowanie wkładem w projekt! Poniżej znajdują się wytyczne dotyczące sposobu współpracy w projektcie.

## Konwencje kodu

### Python

- Użyj **PEP 8** jako standardu kodowania
- Maksymalna długość linii: **100 znaków**
- Nazwy zmiennych i funkcji: **snake_case**
- Nazwy klas: **PascalCase**
- Docstringi: **"""Format docstringu"""**

### Przykład

```python
def get_light_switch_by_id(switch_id: UUID) -> Optional[LightSwitch]:
    """
    Retrieve a light switch by its unique identifier.
    
    Args:
        switch_id: The unique UUID of the light switch.
        
    Returns:
        The LightSwitch object if found, None otherwise.
        
    Raises:
        ValueError: If the switch_id format is invalid.
    """
    # Implementation here
    pass
```

## Commit wiadomości

Używaj jasnych i opisowych commit wiadomości:

### Format

```
<type>: <subject>

<body>

<footer>
```

### Typy commitów

- **feat**: Nowa funkcjonalność
- **fix**: Naprawa błędu
- **docs**: Dokumentacja
- **style**: Formatowanie, brakujące średniki itp.
- **refactor**: Zmiana kodu bez nowych funkcji
- **perf**: Poprawa wydajności
- **test**: Dodanie lub aktualizacja testów
- **chore**: Zmiany w build'cie lub zależnościach

### Przykłady

```bash
git commit -m "feat: Add temperature sensor support

- Implement TemperatureSensor model
- Add MQTT topic for temperature data
- Create API endpoint for reading temperature
- Add unit tests

Closes #42"
```

```bash
git commit -m "fix: Correct MQTT connection timeout

- Increase timeout from 30s to 60s
- Add retry mechanism for failed connections
- Update error handling

Fixes #15"
```

## Gałęzie (Branches)

- `main` - Gałąź główna, ready-to-deploy
- `develop` - Gałąź развития, integracja funkcji
- `feature/*` - Nowe funkcjonalności
- `bugfix/*` - Naprawy błędów
- `docs/*` - Dokumentacja

### Przykład

```bash
git checkout -b feature/temperature-sensor
git checkout -b bugfix/mqtt-reconnection
```

## Pull Requests

### Przed wysłaniem PR

- [ ] Kod przechodzi wszystkie testy (`pytest tests/ -v`)
- [ ] Kod jest sformatowany (`black .`)
- [ ] Brak błędów lintowania (`pylint app/`)
- [ ] Dokumentacja jest aktualna
- [ ] Commity są czyste i dobrze opisane

### Szablon PR

```markdown
## Opis

Krótko opisz czego dotyczy ten PR.

## Typ zmian

- [ ] Nowa funkcjonalność
- [ ] Naprawa błędu
- [ ] Zmiana dokumentacji
- [ ] Refactoring
- [ ] Zmiana wydajności

## Powiązane problemy

Fixes #(issue number)

## Testowanie

Opisz jak testowałeś zmiany.

## Checklist

- [ ] Mój kod przechodzi istniejące testy
- [ ] Dodałem nowe testy dla nowych funkcji
- [ ] Moja dokumentacja jest aktualna
- [ ] Moje commity mają jasne wiadomości
```

## Testowanie

### Wymagania testowe

- Nowe funkcjonalności **muszą** mieć testy
- Naprawy błędów **powinny** mieć test replikujący błąd
- Pokrycie kodu powinno być co najmniej **80%**

### Uruchomianie testów

```bash
# Wszystkie testy
pytest tests/ -v

# Testy z pokryciem
pytest tests/ --cov=app --cov-report=html

# Specyficzny test
pytest tests/test_main.py::test_add_light_switch -v

# Testy z szybkim wyjściem
pytest tests/ -x
```

## Dokumentacja

### Rzeczy do dokumentacji

- Nowe endpointy API
- Nowe modele danych
- Konfiguracja
- Architektura zmian

### Formaty

- README.md - Główna dokumentacja
- Docstringi - Dokumentacja kodu
- Komentarze - Złożona logika

## Testy przed commit'em

```bash
# 1. Uruchom testy
pytest tests/ -v

# 2. Sprawdź formatowanie
black --check app/ simulator/ tests/

# 3. Sprawdź linting
pylint app/

# 4. Sprawdzenie typów (opcjonalne)
mypy app/
```

## Przydatne narzędzia

### Formatowanie kodu

```bash
pip install black
black app/ simulator/ tests/
```

### Linting

```bash
pip install pylint
pylint app/
```

### Type checking

```bash
pip install mypy
mypy app/
```

### Pre-commit hooks

```bash
pip install pre-commit

# Konfiguracja w .pre-commit-config.yaml
pre-commit install
```

## Procedura dla nowych Contributers

1. **Fork** repozytorium
2. **Clone** fork'a na swój komputer
3. **Utwórz** nową gałąź (`feature/my-feature`)
4. **Commit** zmiany z jasnymi wiadomościami
5. **Push** do fork'a
6. **Otwórz** Pull Request z opisem zmian
7. **Respond** do recenzji kodu

## Kod of Conduct

- Bądź szanujący dla pozostałych
- Nie publikuj danych prywatnych
- Nie spam'uj
- Konstruktywna krytyka
- Przebaczyć i zapomnieć

## Pytania?

- GitHub Issues - dla pytań technicznych
- Dyskusje - dla ogólnych pytań
- Email - dla spraw poufnych

## Podziękowania

Dziękujemy za wkład w projekt! 🎉
