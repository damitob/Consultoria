# 🎯 Consulting Interview Prep — Sistema de Emails Automatizados

Sistema que te envía cada semana el contenido de preparación para entrevistas de McKinsey, Bain y BCG.
Generado con IA, adaptado a la semana del programa en que estás.

---

## Cómo funciona

- **Frecuencia:** Cada lunes a las 9am (Buenos Aires, UTC-3)
- **Duración:** 10 semanas
- **Tecnología:** GitHub Actions + Groq API + Gmail SMTP
- **Costo:** Gratis

Cada email incluye: explicación en profundidad de los temas de la semana, ejercicio práctico con instrucciones claras, y recursos recomendados.

---

## Setup — hacés esto una sola vez

### Paso 1 — Groq API Key (gratis)
1. Entrá a [console.groq.com](https://console.groq.com)
2. Creá una cuenta
3. Ve a **API Keys → Create API key**
4. Copiá la key

### Paso 2 — Gmail App Password
1. Andá a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Escribí `Consulting Prep` → click en **Crear**
3. Copiá los 16 caracteres que te genera — no los vas a ver de nuevo

### Paso 3 — Secrets en GitHub
En tu repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `GROQ_API_KEY` | Tu API key de Groq |
| `GMAIL_USER` | Tu Gmail completo (ej: tumail@gmail.com) |
| `GMAIL_APP_PASSWORD` | Los 16 caracteres del paso anterior |
| `RECIPIENT_EMAIL` | Donde querés recibir los emails |
| `START_DATE` | Fecha de inicio en formato `YYYY-MM-DD` (ej: `2026-06-18`) |

### Paso 4 — Probá que funciona
1. En tu repo → **Actions → Consulting Prep — Weekly Email**
2. Click en **Run workflow → Run workflow**
3. Esperá ~60 segundos
4. Si llega el email de la Semana 1, el sistema está funcionando

A partir de ahí llega solo cada lunes. No tenés que hacer nada más.

---

## Estructura del programa

| Semana | Foco |
|--------|------|
| 1 | Qué es un case y cómo piensan las consultoras |
| 2 | Frameworks y pensamiento estructurado (MECE) |
| 3 | Mental math y estimaciones de mercado |
| 4 | Primera práctica: profitability cases |
| 5 | Market sizing y market entry |
| 6 | Partner practice y feedback |
| 7 | Cases avanzados: M&A, pricing, operational |
| 8 | Integración y corrección de patrones |
| 9 | Fit stories y PEI |
| 10 | Mock interview final y aplicación |

---

## Troubleshooting

**Error de autenticación Gmail**
→ Verificá que la verificación en 2 pasos está activa y que copiaste bien los 16 caracteres. No uses tu contraseña normal de Gmail.

**Error de Groq API**
→ Verificá que la key está bien copiada y que tu cuenta de Groq está activa.

**El workflow muestra verde pero no llega el email**
→ Revisá spam. Verificá que `RECIPIENT_EMAIL` está bien escrito.

**Quiero recibir el email de una semana específica**
→ Cambiá temporalmente `START_DATE` a una fecha que haga caer en esa semana y ejecutá manualmente.

---

## Archivos del proyecto

```
consulting-prep/
├── .github/
│   └── workflows/
│       └── prep-mailer.yml
├── scripts/
│   └── send_prep.py
└── README.md
```
