# Drip-Sense Dashboard

Real-time web-based control center for monitoring all IV drip devices.

## Tech Stack

- **Next.js 14** (React, App Router)
- **Tailwind CSS 3** (styling)
- **Recharts** (charts)
- **Socket.IO / MQTT.js** (real-time data)
- **Zustand** (state management)
- **Prisma** (database ORM)
- **NextAuth.js** (authentication)

## Pages

| Page | URL | Description |
|---|---|---|
| Login | `/login` | Role-based authentication |
| Dashboard Home | `/dashboard` | Ward overview with bed cards |
| Patient Management | `/patients` | Patient database (CRUD) |
| Patient Detail | `/patients/[patientId]` | Live monitoring & history |
| Alert Center | `/alerts` | Alarm management |
| Analytics | `/analytics` | Reports & trends |
| Device Management | `/devices` | ESP32 device config |
| Settings | `/settings` | System configuration |

## Getting Started

```bash
npm install
cp .env.example .env.local
npx prisma migrate dev
npm run dev
```

Dashboard available at http://localhost:3000
