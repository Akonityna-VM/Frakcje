# 🤖 Frakcje – Discord Bot

Bot do zarządzania frakcjami w społeczności Discord. Gracze wybierają frakcje, zdobywają XP, poziomy i punkty frakcyjne poprzez udział w wydarzeniach i wykonywanie dziennych misji.  
Bot automatycznie nadaje role poziomowe, prowadzi rankingi oraz zapewnia panel administracyjny.

---

## 🛠️ Funkcje

### 🧾 Zarządzanie frakcjami
- `!frakcje` – wybór frakcji przez reakcję emoji (jednorazowy)
- `!resetfrakcja @użytkownik` – reset frakcji i ról użytkownika

### 🧠 XP i poziomy
- `!dodajxp @użytkownik <liczba>` – dodaje XP i poziomuje
- `!odejmijxp @użytkownik <liczba>` – odejmuje XP i aktualizuje poziom
- `!resetxp @użytkownik` – resetuje XP i poziom
- `!poziom [@użytkownik]` – pokazuje poziom, XP i frakcję

### 🎯 Misje dzienne
- `!misja` – losowa misja raz na 24h (XP + punkty frakcji)

### 🏆 Ranking i punkty frakcji
- `!punktyfrakcji` – aktualne wyniki frakcji
- `!dodajfrakcji <frakcja> <liczba>` – dodaje punkty konkretnej frakcji
- `!ranking [frakcja]` – TOP 10 graczy globalnie lub we frakcji

### 📊 Panel Administratora
- `!paneladmin` – embed z danymi: liczba graczy, średni XP i poziom, punkty frakcji

### 🔍 Komendy informacyjne
- `!mojafrakcja` – frakcja, XP i poziom gracza
- `!mojerole` – lista aktualnych ról gracza

---

## 🔐 Uprawnienia

Komendy administracyjne (`!dodajxp`, `!odejmijxp`, `!resetxp`, `!resetfrakcja`, `!paneladmin`) wymagają uprawnień:
- **Zarządzanie wiadomościami** lub
- **Administrator**

Pozostałe komendy są dostępne dla wszystkich użytkowników.

---

## 🚀 Uruchamianie bota

> Aktualnie bot nie jest jeszcze skonfigurowany pod Railway, ale będzie uruchamiany automatycznie po wdrożeniu.

Tymczasowo możesz uruchomić go lokalnie:

```bash
python bot.py
