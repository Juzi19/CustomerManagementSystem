# Customer Management System (CMS)

Dies ist ein Customer Management System, das mit **Django** entwickelt wurde. Es ermöglicht die Verwaltung von Kundeninformationen, die Kommunikation über ein internes Chat-System und die Verwaltung von Projekten. Die Anwendung umfasst grundlegende Funktionen wie die Erstellung, Bearbeitung und Löschung von Kunden sowie ein Echtzeit-Chat-System für die Kommunikation mit den Kunden.

## Features

- **Benutzerverwaltung**: Erstellen, Bearbeiten und Löschen von Kunden.
- **Chat-System**: Echtzeit-Kommunikation mit Kunden über WebSockets.
- **Projektverwaltung**: Verwalten von Projekten für jeden Kunden.
- **Benachrichtigungen**: Wichtige Ereignisse werden in Echtzeit angezeigt.
- **REST API**: Für die Interaktion mit externen Systemen oder mobilen Anwendungen.
- **Admin Interface**: Verwaltbarkeit über das Django Admin Interface.

## Technologien

- **Backend**: Django
- **Datenbank**: PostgreSQL (kann in den Einstellungen angepasst werden)
- **Frontend**: HTML, CSS, JavaScript (optional: React für fortgeschrittene Features)
- **Realtime-Chat**: WebSockets (über Django Channels)
- **Auth**: Benutzer-Authentifizierung (Django's User-Modell)
- **Zahlung**: (Optional) Stripe für Zahlungsabwicklung

## Installation

### 1. Klone das Repository:
```bash
git clone https://github.com/deinbenutzername/customer-management-system.git
cd customer-management-system
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
