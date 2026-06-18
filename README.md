# 🎯 Consulting Interview Prep — Sistema de Emails Automatizados

Sistema que te envía cada semana el contenido de preparación para entrevistas de McKinsey, Bain y BCG.
Generado con IA, adaptado a la semana del programa en que estás.

---

## Cómo funciona

- **Frecuencia:** Cada lunes a las 9am (Buenos Aires, UTC-3)
- **Duración:** 10 semanas
- **Tecnología:** GitHub Actions + Anthropic API + Gmail SMTP
- **Costo estimado:** ~$2 USD en créditos de API para todo el programa

Cada email incluye: explicación en profundidad de los temas de la semana, ejercicio práctico con instrucciones claras, y recursos recomendados.

---

## Setup — hacés esto una sola vez (15 minutos)

### Paso 1 — Creá el repositorio en GitHub

1. Entrá a [github.com](https://github.com) y hacé click en **New repository**
2. Nombre: `consulting-prep` (o el que quieras)
3. Marcalo como **Private**
4. Crealo sin README
5. Subí los archivos de este proyecto al repositorio

Para subir los archivos, podés hacerlo desde la interfaz web de GitHub:
- Entrá al repo → **Add file → Upload files**
- Subí `scripts/send_prep.py` y `.github/workflows/prep-mailer.yml` respetando la estructura de carpetas

O si tenés Git instalado:
```bash
cd consulting-prep
git init
git remote add origin https://github.com/TU_USUARIO/consulting-prep.git
git add .
git commit -m "Setup inicial"
git push -u origin main
```

---

### Paso 2 — Conseguí tu Anthropic API Key

1. Entrá a [console.anthropic.com](https://console.anthropic.com) y creá una cuenta
2. Ve a **API Keys → Create Key**
3. Copiá la key (la vas a ver una sola vez)
4. Ve a **Billing → Add credits** y cargá $5 USD (alcanza para todo el programa)

---

### Paso 3 — Configurá Gmail para envío automático

Gmail no te deja usar tu contraseña normal para enviar emails por código.
Tenés que crear una "contraseña de aplicación":

1. En tu cuenta Google → **Cuenta → Seguridad**
2. Activá **Verificación en 2 pasos** (si no la tenés)
3. Buscá **Contraseñas de aplicaciones** (aparece solo si el paso 2 está activo)
4. Creá una nueva → Aplicación: "Otro" → Nombre: "Consulting Prep"
5. Google te genera 16 caracteres → **copiálos ahora**, no los vas a ver de nuevo

---

### Paso 4 — Agregá los 5 Secrets en GitHub

En tu repositorio: **Settings → Secrets and variables → Actions → New repository secret**

Agregá estos 5 uno por uno:

| Secret | Qué es | Ejemplo |
|--------|--------|---------|
| `ANTHROPIC_API_KEY` | Tu API key de Anthropic | `sk-ant-api03-...` |
| `GMAIL_USER` | Tu email de Gmail | `tumail@gmail.com` |
| `GMAIL_APP_PASSWORD` | Los 16 caracteres del paso anterior | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | Donde querés recibir los emails | `tumail@gmail.com` |
| `START_DATE` | Fecha de inicio del programa | `2026-06-18` |

> Para `GMAIL_APP_PASSWORD`: copiá los 16 caracteres tal como aparecen, con o sin espacios.

---

### Paso 5 — Probá que todo funciona

1. En tu repo → **Actions → Consulting Prep — Weekly Email**
2. Click en **Run workflow → Run workflow**
3. Esperá ~60 segundos
4. Si el workflow muestra ✅ verde, revisá tu casilla de email

Si recibís el email de la Semana 1, el sistema está funcionando. No tenés que hacer nada más.
Los emails siguientes van a llegar solos cada lunes.

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

**El workflow falla con error de autenticación Gmail**
→ Verificá que activaste la verificación en 2 pasos y que copiaste bien los 16 caracteres.
→ No uses tu contraseña normal de Gmail — tiene que ser la contraseña de aplicación.

**El workflow falla con error de Anthropic**
→ Verificá que tu API key es válida (empieza con `sk-ant-`) y que tenés créditos cargados.

**Quiero recibir el email de una semana específica (no la que corresponde)**
→ Temporalmente cambiá el Secret `START_DATE` a la fecha que haría que caiga en esa semana.
→ Ejemplo: si querés la Semana 3, poné como START_DATE una fecha de 14 días atrás.
→ Ejecutá manualmente. Después volvé a poner la fecha original.

**El workflow muestra verde pero no recibí el email**
→ Revisá spam/correo no deseado.
→ Verificá que `RECIPIENT_EMAIL` está bien escrito.

**Ya pasaron las 10 semanas y quiero repetir el programa**
→ Actualizá `START_DATE` con la fecha de hoy y ejecutá manualmente.

---

## Archivos del proyecto

```
consulting-prep/
├── .github/
│   └── workflows/
│       └── prep-mailer.yml    ← el automatizador
├── scripts/
│   └── send_prep.py           ← la lógica principal
└── README.md                  ← este archivo
```
