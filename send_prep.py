#!/usr/bin/env python3
"""
Consulting Interview Prep — Automated Weekly Email
McKinsey / Bain / BCG preparation system
"""

import anthropic
import smtplib
import os
import sys
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────────────────────
# CURRICULUM — 10 semanas de preparación
# ─────────────────────────────────────────────────────────────

CURRICULUM = {
    1: {
        "titulo": "Qué es un case y cómo piensan las consultoras",
        "subtitulo": "El mapa antes del territorio",
        "contexto": (
            "Esta semana no practicás cases. Tu único objetivo es entender el juego antes de jugarlo. "
            "La mayoría de candidatos llega a sus primeros cases sin entender qué evalúa el entrevistador. "
            "Eso se paga caro."
        ),
        "temas": [
            "Cómo funciona el proceso de selección en McKinsey, Bain y BCG (son distintos entre sí)",
            "Qué evalúa el entrevistador — spoiler: no es si 'resolvés' el case",
            "La estructura de una entrevista típica de 45-60 minutos",
            "Por qué los frameworks importan y cuándo NO usarlos",
            "El mindset correcto: consultor, no adivino",
        ],
        "ejercicio": (
            "Leé 2 cases resueltos completos en CaseInterview.com (Victor Cheng) SIN intentar resolverlos. "
            "Solo observá. Después escribí 3 observaciones concretas sobre cómo el candidato estructura "
            "su respuesta, cuándo hace preguntas y cómo comunica mientras piensa. "
            "Guardá esas 3 observaciones — las vamos a usar la semana que viene."
        ),
        "recursos": [
            "CaseInterview.com — Victor Cheng (gratuito, empezá por ahí)",
            "YouTube: 'McKinsey case interview examples' — canal oficial de McKinsey",
            "Libro: Case in Point — Marc Cosentino (opcional, no urgente esta semana)",
        ],
    },
    2: {
        "titulo": "Frameworks y pensamiento estructurado",
        "subtitulo": "MECE, issue trees y los frameworks que sí importan",
        "contexto": (
            "El 80% de los candidatos que no pasan cases tienen el mismo problema: estructuran mal. "
            "No porque no sean inteligentes, sino porque nunca aprendieron a pensar en forma MECE. "
            "Esta semana es la más importante conceptualmente de todo el programa."
        ),
        "temas": [
            "MECE: qué significa, por qué importa y ejemplos donde falla",
            "Issue trees: cómo descomponer un problema en partes sin superposición ni agujeros",
            "Framework de rentabilidad (Ingresos / Costos) — la base de casi todos los cases",
            "Framework de entrada a mercado — las 3 preguntas que siempre tenés que responder",
            "Cuándo usar frameworks y cuándo inventar tu propia estructura",
        ],
        "ejercicio": (
            "Problema: 'Las ganancias de una cadena de farmacias cayeron 15% en el último año.' "
            "Armá un issue tree MECE con al menos 3 niveles de profundidad. "
            "Hacelo en papel o en un documento — no busques respuestas en internet. "
            "Guardalo para mostrármelo la próxima vez que hablemos."
        ),
        "recursos": [
            "PrepLounge.com — cases gratuitos con comunidad activa",
            "Video: 'MECE Framework Explained' — MConsultingPrep en YouTube",
        ],
    },
    3: {
        "titulo": "Mental math y estimaciones de mercado",
        "subtitulo": "El talón de Aquiles de muchos candidatos con experiencia laboral",
        "contexto": (
            "La matemática en cases no es difícil conceptualmente. Lo difícil es hacerla bien, "
            "rápido y en voz alta mientras pensás en el problema. "
            "Si tardás demasiado o pedís calculadora, perdés puntos. Esta semana la dedicás a esto."
        ),
        "temas": [
            "Técnicas de mental math para números grandes en cases",
            "Market sizing: approach top-down vs bottom-up (y cuándo usar cada uno)",
            "Cómo comunicar tu razonamiento mientras calculás — nunca te quedes en silencio",
            "Redondeo inteligente: cuándo es aceptable y cómo hacerlo sin perder precisión",
            "Los 5 datos de memoria que necesitás tener (población, PBI, etc.)",
        ],
        "ejercicio": (
            "Estimá estos dos mercados SIN buscar datos en internet. Mostrá tu razonamiento paso a paso:\n"
            "1. ¿Cuántos autos nuevos se venden en Argentina por año?\n"
            "2. ¿Cuál es el mercado anual de café en cadenas de cafeterías en Buenos Aires (en pesos)?\n\n"
            "Extra: practicá multiplicaciones de 2 dígitos × 2 dígitos 5 minutos por día. "
            "App recomendada: Math Workout."
        ),
        "recursos": [
            "App: Math Workout o Mental Math Master (iOS/Android, gratis)",
            "Datos útiles para memorizar: Argentina ~46M hab, CABA ~3M, salario medio ~$600K ARS mensual",
        ],
    },
    4: {
        "titulo": "Primera práctica real: profitability cases",
        "subtitulo": "Arrancás a practicar. En voz alta. Solo.",
        "contexto": (
            "Esta semana hacés tu primer case real. Solo, en voz alta. "
            "Sí, en voz alta aunque estés solo — la práctica silenciosa no te prepara para la entrevista. "
            "Los cases de rentabilidad son los más comunes y los mejores para empezar."
        ),
        "temas": [
            "Cómo abrir un case correctamente — los primeros 60 segundos son críticos",
            "Cuándo pedir tiempo para estructurar y cómo usarlo bien",
            "Cómo navegar el case cuando tu hipótesis inicial no funciona",
            "Cómo cerrar con una recomendación clara y accionable (no 'depende')",
            "Los 5 errores más comunes en profitability cases",
        ],
        "ejercicio": (
            "Case: 'Tu cliente es una empresa de e-commerce de moda en Argentina. "
            "Sus márgenes cayeron del 18% al 8% en 2 años a pesar de que las ventas crecieron 40%. "
            "¿Qué pasó y qué le recomendás?'\n\n"
            "Resolverlo solo en voz alta. Grabate con el teléfono (solo audio está bien). "
            "Escuchate después. Mandame tu estructura inicial y tu conclusión final."
        ),
        "recursos": [
            "PrepLounge.com — filtrá por 'Profitability' y nivel 'Beginner'",
            "RocketBlocks.me — tiene feedback automatizado (freemium)",
        ],
    },
    5: {
        "titulo": "Market sizing y market entry",
        "subtitulo": "Dos tipos de case que requieren approach distinto",
        "contexto": (
            "Ya tenés la base del framework de rentabilidad. Ahora sumás dos tipos de case "
            "que aparecen constantemente y que son estructuralmente distintos. "
            "El market entry en particular es muy común en McKinsey."
        ),
        "temas": [
            "Market sizing: las dos approaches y cómo elegir entre ellas",
            "Cómo construir hipótesis desde el principio — no lanzarte a calcular",
            "Las 4 preguntas clave de un market entry case",
            "Cómo integrar análisis cualitativo y cuantitativo en el mismo case",
            "Trampas comunes: olvidar el 'so what', no dimensionar el mercado, ignorar competidores",
        ],
        "ejercicio": (
            "Case: 'Una empresa de seguros de salud quiere ingresar al mercado de seguros para mascotas en Chile. "
            "¿Deberían hacerlo? Si sí, cómo?'\n\n"
            "Antes de resolver: escribí qué información le pedirías al entrevistador y por qué (lista de 5-7 preguntas). "
            "Luego resolvelo en voz alta y guardá tu estructura inicial."
        ),
        "recursos": [
            "YouTube: Bain & Company case interview examples — canal oficial",
            "PrepLounge: filtrá por 'Market Entry' y 'Market Sizing'",
        ],
    },
    6: {
        "titulo": "Partner practice: la práctica que más importa",
        "subtitulo": "Encontrá un partner esta semana. No es opcional.",
        "contexto": (
            "Practicar solo tiene un límite: no te prepara para la incomodidad de tener a alguien "
            "enfrente mirándote mientras pensás. Esa incomodidad es exactamente lo que vas a enfrentar. "
            "Tu misión esta semana: encontrá un partner y hacé al menos 2 cases juntos."
        ),
        "temas": [
            "Dónde encontrar partners de práctica (PrepLounge, Reddit, LinkedIn)",
            "Cómo dar feedback útil como entrevistador — es una habilidad que se aprende",
            "Qué buscar cuando recibís feedback y cómo no ponerte defensivo",
            "Cómo simular condiciones reales: sin notas, en voz alta, con timing",
            "Métricas de evaluación: en qué dimensiones calificar un case",
        ],
        "ejercicio": (
            "Hacé al menos 2 mock cases con un partner esta semana.\n"
            "Después de cada uno, pedile que te califique del 1-5 en:\n"
            "→ Estructura inicial\n→ Razonamiento\n→ Math\n→ Comunicación\n→ Conclusión\n\n"
            "Guardá los números. La próxima vez que hablemos los usamos para identificar tu punto débil."
        ),
        "recursos": [
            "PrepLounge.com → sección 'Case Partner Matching'",
            "Reddit r/consulting → buscá 'practice partner' threads",
            "LinkedIn: grupos de 'case interview practice Latam'",
        ],
    },
    7: {
        "titulo": "Cases avanzados: M&A, pricing y operational",
        "subtitulo": "Menos frecuentes, pero los que diferencian candidatos",
        "contexto": (
            "Ya dominás los tipos de case más comunes. Ahora los que aparecen menos seguido "
            "pero que los candidatos sin preparación específica pierden. "
            "Si llegás a una entrevista de McKinsey con un M&A case y no lo preparaste, se nota."
        ),
        "temas": [
            "Framework para evaluar una adquisición — estratégico + financiero + integración",
            "Pricing cases: cost-plus vs value-based vs competitive pricing",
            "Operational cases: cuándo y cómo analizar eficiencia de procesos",
            "Cómo manejar datos ambiguos o incompletos — te los van a dar así a propósito",
            "Creatividad dentro de estructura: cómo mostrar pensamiento propio sin perder el hilo",
        ],
        "ejercicio": (
            "Case: 'Una empresa de alimentos quiere adquirir una startup de delivery de comida saludable "
            "que factura $5M anuales pero pierde $2M. ¿Le recomendás que proceda?'\n\n"
            "Foco especial: antes de estructurar tu análisis, hacé una lista de las preguntas "
            "que harías al cliente y justificá por qué cada una importa."
        ),
        "recursos": [
            "McKinsey Insights — leé 3 artículos de industrias que no conocés bien esta semana",
            "Harvard Business Review — sección de M&A y Strategy",
        ],
    },
    8: {
        "titulo": "Integración y corrección de patrones",
        "subtitulo": "Identificá tus errores recurrentes — ahí está tu mayor ganancia",
        "contexto": (
            "A esta altura ya hiciste entre 8 y 12 cases. Esta semana no aprendés cosas nuevas. "
            "Es para hacer una autopsia honesta de tus patrones de error. "
            "Todo el mundo tiene 2-3 errores recurrentes. El que los identifica y los trabaja "
            "específicamente es el que pasa."
        ),
        "temas": [
            "Cómo hacer una autopsia honesta de tus cases anteriores",
            "Los 5 errores más comunes en candidatos con experiencia laboral en esta etapa",
            "Cómo manejar el bloqueo mental durante un case — y que no se note",
            "Síntesis ejecutiva: cómo dar recomendaciones con confianza aunque no estés seguro",
            "Calibración: cómo saber si tu nivel actual es suficiente para aplicar",
        ],
        "ejercicio": (
            "Revisá todos los cases que hiciste hasta ahora y respondé:\n"
            "¿Cuál es TU error más frecuente? (estructura, math, comunicación, conclusión, otro)\n\n"
            "Hacé 2 cases con partner esta semana poniendo foco ESPECÍFICO en corregir ese punto. "
            "Después contame qué identificaste y cómo te fue."
        ),
        "recursos": [
            "Opcional: sesión de 1h con coach ex-McKinsey/Bain en PrepLounge (€50-100)",
            "Solo si sentís que llegaste a un techo con la práctica entre pares.",
        ],
    },
    9: {
        "titulo": "Fit stories: tu historia personal",
        "subtitulo": "El 50% de la entrevista que la mayoría subestima",
        "contexto": (
            "McKinsey llama a esta parte PEI (Personal Experience Interview). Bain también la evalúa en profundidad. "
            "Muchos candidatos con buenos cases no pasan porque llegan sin historias trabajadas o suenan guionados. "
            "Tenés experiencia laboral real — esa es tu ventaja. Hay que trabajarla."
        ),
        "temas": [
            "Qué evalúa el PEI: liderazgo personal, influencia sin autoridad, impacto en resultados",
            "El método STAR adaptado a consultoría — con las diferencias que importan",
            "Cómo usar tu experiencia laboral aunque no sea de consultoría",
            "Por qué suenan guionados los candidatos y cómo evitarlo",
            "Las preguntas de profundización que te van a hacer (las que dejan a muchos sin respuesta)",
        ],
        "ejercicio": (
            "Escribí — no en tu cabeza, en texto — 3 historias profesionales reales que respondan:\n"
            "1. 'Contame de una situación donde lideraste algo difícil'\n"
            "2. 'Contame de una situación donde tuviste que influir sin autoridad formal'\n"
            "3. 'Contame del mayor impacto que tuviste en un proyecto'\n\n"
            "Cada historia: máximo 4 párrafos. Traeme las 3 y te doy feedback concreto."
        ),
        "recursos": [
            "Practicá con un amigo: que te pregunte '¿y vos específicamente qué hiciste?' después de cada respuesta",
            "Esa pregunta es exactamente lo que McKinsey y Bain usan para filtrar candidatos que exageran su rol",
        ],
    },
    10: {
        "titulo": "Simulacro final y aplicación",
        "subtitulo": "Llegaste. Ahora aplicá.",
        "contexto": (
            "Esta semana no aprendés cosas nuevas. Consolidás, simulás condiciones reales "
            "y entrás con confianza. El objetivo de esta semana es uno solo: aplicar."
        ),
        "temas": [
            "Mock interview completo: case + fit en 45 minutos cronometrados",
            "Cómo estructurar tu día antes de una entrevista real",
            "Manejo de nervios y síndrome del impostor — es normal, no te paralices",
            "El proceso de aplicación actual en McKinsey, Bain y BCG Argentina",
            "Cómo escribir el email de networking antes de aplicar (puede hacer diferencia)",
        ],
        "ejercicio": (
            "Hacé UN mock interview completo con un partner que incluya:\n"
            "→ 5 min: preguntas de fit (¿por qué consultoría? ¿por qué esta firma?)\n"
            "→ 30 min: case completo\n"
            "→ 10 min: PEI con una de tus historias\n\n"
            "Grabalo. Miralo. Identificá los últimos ajustes.\n\n"
            "Y después: APLICÁ. Esta es la semana."
        ),
        "recursos": [
            "McKinsey Careers Argentina: mckinsey.com/careers",
            "Bain Argentina: bain.com/careers",
            "BCG Argentina: bcg.com/careers",
            "Oliver Wyman y Strategy& también entrevistan con cases y están en Buenos Aires",
        ],
    },
}


# ─────────────────────────────────────────────────────────────
# LÓGICA PRINCIPAL
# ─────────────────────────────────────────────────────────────

def get_current_week() -> int:
    start_date_str = os.environ.get("START_DATE", "").strip()
    if not start_date_str:
        print("ERROR: La variable START_DATE no está configurada.")
        sys.exit(1)

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"ERROR: START_DATE tiene formato incorrecto: '{start_date_str}'. Usá YYYY-MM-DD.")
        sys.exit(1)

    today = date.today()
    days_elapsed = (today - start_date).days

    if days_elapsed < 0:
        print("ERROR: START_DATE está en el futuro.")
        sys.exit(1)

    week = (days_elapsed // 7) + 1

    if week > 10:
        print(f"Programa completado. Han pasado {days_elapsed} días desde el inicio. Felicitaciones — ahora aplicá.")
        sys.exit(0)

    return week


def generate_email_html(week_num: int, week_data: dict) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    temas_str = "\n".join(f"- {t}" for t in week_data["temas"])
    recursos_str = "\n".join(f"- {r}" for r in week_data["recursos"])

    prompt = f"""
Sos un coach de preparación para entrevistas de consultoría estratégica (McKinsey, Bain, BCG).
Estás escribiendo el email semanal para un candidato en la SEMANA {week_num} de 10.
El candidato es un profesional argentino con experiencia laboral que quiere ingresar a una top consultora.

ESTRUCTURA DE ESTA SEMANA:
- Título: {week_data["titulo"]}
- Subtítulo: {week_data["subtitulo"]}
- Contexto: {week_data["contexto"]}
- Temas a cubrir en profundidad:
{temas_str}
- Ejercicio de la semana:
{week_data["ejercicio"]}
- Recursos:
{recursos_str}

INSTRUCCIONES:
1. Apertura directa y concreta — no genérica
2. Desarrollá cada tema con profundidad: ejemplos, errores comunes, por qué importa
3. Presentá el ejercicio claramente con todos los detalles
4. Listá los recursos
5. Cierre de 1-2 líneas, sin motivación vacía

TONO: Directo, sin condescender. Como un ex-consultor que habla de igual a igual.
Sin "¡Excelente!", "¡Vamos!", ni frases motivacionales. Tuteás (español rioplatense). Sé sustancioso.

FORMATO HTML COMPLETO:
- max-width: 600px, centrado, fondo blanco (#ffffff)
- Texto: #1a1a1a, font-family: Arial, sans-serif
- Títulos de sección: con border-left 3px sólido #1e3a5f
- Ejercicio: en un box con fondo #eef2f7, borde izquierdo #1e3a5f
- Sin emojis excepto máximo 2-3 donde genuinamente aporten
- HTML completo y renderizable en cliente de email

Solo devolvé el HTML. Sin texto adicional antes ni después.
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def send_email(html_content: str, week_num: int, week_title: str):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Semana {week_num}/10] Prep Consultoría: {week_title}"
    msg["From"] = f"Consulting Prep <{gmail_user}>"
    msg["To"] = recipient

    plain = (
        f"Semana {week_num}/10 — {week_title}\n"
        "Abrí este email en un cliente que soporte HTML para ver el contenido completo."
    )
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, recipient, msg.as_string())
        print(f"Email Semana {week_num} enviado correctamente a {recipient}")
    except Exception as e:
        print(f"ERROR al enviar email: {e}")
        sys.exit(1)


def main():
    required_vars = ["ANTHROPIC_API_KEY", "GMAIL_USER", "GMAIL_APP_PASSWORD", "RECIPIENT_EMAIL", "START_DATE"]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        print(f"ERROR: Faltan variables de entorno: {', '.join(missing)}")
        sys.exit(1)

    week_num = get_current_week()
    week_data = CURRICULUM[week_num]

    print(f"Generando email — Semana {week_num}: {week_data['titulo']}")
    html = generate_email_html(week_num, week_data)
    send_email(html, week_num, week_data["titulo"])
    print("Listo.")


if __name__ == "__main__":
    main()
