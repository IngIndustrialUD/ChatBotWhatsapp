import os
import requests
from urllib.parse import quote_plus
from flask import Flask, request
from flask import send_from_directory
app = Flask(__name__)

@app.get("/privacy.html")
def privacy():
    # Sirve el archivo privacy.html que está en la misma carpeta de app.py
    return send_from_directory(".", "privacy.html")

# ========= CONFIG =========
#VERIFY_TOKEN   = os.getenv("VERIFY_TOKEN", 127e13f38859fc267bf1382aac65a0e8 )
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN","mi_token_de_verificacion")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "REEMPLAZA_CON_TU_TOKEN")
API_VERSION    = os.getenv("WHATSAPP_API_VERSION", "v20.0")

# Logo (URL pública directa, p. ej. RAW de GitHub)
LOGO_URL_UD = os.getenv("LOGO_URL_UD", "")

# ========= HELPERS =========
def graph_post(path: str, payload: dict):
    url = f"https://graph.facebook.com/{API_VERSION}/{path}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    print("Graph POST:", r.status_code)
    try:
        print("Graph RESP:", r.json())
    except Exception:
        print("Graph RESP (raw):", r.text[:500])
    return r

def send_text(phone_number_id: str, to: str, text: str):
    return graph_post(f"{phone_number_id}/messages", {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    })

def send_image_with_caption(phone_number_id: str, to: str, image_url: str, caption: str = ""):
    if not image_url:
        return None
    return graph_post(f"{phone_number_id}/messages", {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": image_url, "caption": caption}
    })


def button_message(phone_number_id: str, to: str, header: dict, body_text: str, buttons: list, footer_text: str = ""):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {"buttons": buttons}
        }
    }
    if footer_text:
        payload["interactive"]["footer"] = {"text": footer_text}
    if header:
        payload["interactive"]["header"] = header
    return graph_post(f"{phone_number_id}/messages", payload)

def qr_link(data: str, size: str = "512x512") -> str:
    # Se conserva por compatibilidad, pero se dejó de usar donde el documento pide "sin QR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}&data={quote_plus(data)}"

# ========= BIENVENIDA + MENÚ (3 tarjetas) =========
BIENVENIDA = (
    "*Chat Institucional*\n"
    "*Proyecto Curricular de Ingeniería Industrial*\n"
    "*Universidad Distrital Francisco José de Caldas*"
)

def send_welcome(phone_number_id: str, to: str):
    # Logo SOLO aquí (no en el menú)
    if LOGO_URL_UD:
        send_image_with_caption(phone_number_id, to, LOGO_URL_UD,BIENVENIDA)
    else:
        send_text(phone_number_id, to, BIENVENIDA)

def send_menu_buttons_all(phone_number_id: str, to: str):
    """
    Envía 3 mensajes tipo botón (3 opciones por mensaje = 9 en total).
    Sin logo ni header en las tarjetas (solo en el saludo).
    *** NO se elimina ningún menú, por solicitud del usuario. ***
    """
    # Tarjeta TRÁMITES (1–3)
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Menú · Trámites*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_1", "title": "Cancelación/Aplaz."}},
            {"type": "reply", "reply": {"id": "op_2", "title": "Reintegro"}},
            {"type": "reply", "reply": {"id": "op_3", "title": "Inscr./Cancel. Asig."}}
        ],
        footer_text=""
    )

    # Tarjeta (renombrada) TRABAJO DE GRADO (4–6)
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Menú · Trabajo de grado*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_4", "title": "Trabajo de grado"}},
            {"type": "reply", "reply": {"id": "op_5", "title": "Práctica empresarial"}},  # reemplaza RIUD
            {"type": "reply", "reply": {"id": "op_6", "title": "Actas de consejo"}}       # renombrado
        ],
        footer_text=""
    )

    # Tarjeta OTROS (7–9)
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Menú · Otros*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_7", "title": "Constancias/Notas"}},
            {"type": "reply", "reply": {"id": "op_8", "title": "Correo modelo"}},
            {"type": "reply", "reply": {"id": "op_9", "title": "Paz y salvos"}}
        ],
        footer_text=""
    )

def send_back_to_menu_button(phone_number_id: str, to: str):
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Desea volver al menú?",
        buttons=[{"type": "reply", "reply": {"id": "menu", "title": "Menú"}}],
        footer_text=""
    )

# ========= LINKS (texto plano; sin QR donde se solicita) =========
LINK_RIUD       = "https://repositorio.udistrital.edu.co"
LINK_LABS       = ("https://is.gd/LK3evv")
LINK_BIBLIO     = "https://bibliotecas.udistrital.edu.co/servicios/paz_y_salvos"
LINK_BIENESTAR  = "https://bienestar.udistrital.edu.co/node/634"

# Reintegro (Admisiones)
LINK_ADMISIONES = "https://www.udistrital.edu.co/admisiones/index.php/"

# Constancias — Derechos pecuniarios
LINK_DERECHOS   = "https://udistritaleduco-my.sharepoint.com/:b:/g/personal/ingelectronica_udistrital_edu_co/IQBjnQKmTrmqQalzP7OjGy2dAXh42bB_YkTClgZCxsUDEQc?e=vJUu7k"

# Trabajo de grado — (se conserva banner; se ajustan formularios y textos)
TG_FORM_1   = "https://forms.office.com/r/8ZkpzjTYvX"   # Acta sustentación (3 días antes)
TG_FORM_3   = "https://forms.office.com/r/0r0hjX0Bh4"   # Permiso RIUD (tras inscripción)
TG_FORM_4   = "https://forms.office.com/r/P81G4Fqt0A"   # Práctica empresarial (form base)
TG_BANNER   = "https://udistritaleduco-my.sharepoint.com/:b:/g/personal/ingelectronica_udistrital_edu_co/EQRfFbhqDKlPsIdKzjKL_HsBkYzq5JBC7PBkqlxDFU0TFQ?e=MXNNwn"
RIUD_GUIA   = "https://repository.udistrital.edu.co/assets/custom/docs/Guia_RIUD_autor.pdf"

# Práctica empresarial — links de soporte
PE_FORMATO_SOLIC = "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/EeGl6EoBDpJNuxKg6PqYJrwBZhx6TYivnL7uRWKco_D_LA?e=ig9DQu"
PE_CARTA_TUTOR   = "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/EXp2Pl4gjFBDoIksXo_7_dYBwh8z_V6KO4D466Jr9A6biw?e=DboPOo"
PE_INFORME       = "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/Ea6rADiXua9FjuiE6B0ViGsBJ-Kc217eO1-9e-4LpS0hMw?e=IJ27L3"

# ========= RESPUESTAS (formales, ajustadas al documento) =========
R1 = (
    "*Cancelación o Aplazamiento*\n\n"
    "*Aplazamiento (Semanas 1–2):* Enviar solicitud a *ingelectronica@udistrital.edu.co*, "
    "adjuntando *carta de motivos firmada* y paz y salvo de *Laboratorios, Bienestar y Biblioteca*.\n"
    f"• Laboratorios: {LINK_LABS}\n"
    f"• Bienestar: {LINK_BIENESTAR}\n"
    f"• Biblioteca: {LINK_BIBLIO}\n\n"
    "*Cancelación (Semanas 3–8):* Enviar solicitud a *secing@udistrital.edu.co* con los mismos soportes "
    "(carta firmada y paz y salvos).\n\n"
    "🔁 *Ambos procesos permiten regresar maximo después de un año.*\n"
    "⚠️ Si no haces el trámite, el sistema puede marcar *abandono*.\n\n"
    "📌 *Nota:* la decisión final corresponde al *Consejo de Facultad*."
)

R2 = (
    "*Reintegro*\n\n"
    "1) Debes estar pendiente de la página de *Admisiones*:\n"
    f"👉 {LINK_ADMISIONES}\n"
    "2) Allí se anuncia cuándo está habilitado el proceso.\n"
    "3) Tendrás que comprar un *PIN de reintegro*, usualmente disponible *mes y medio* antes de finalizar el semestre en curso.\n"
    "4) La publicación del proceso normalmente se hace *dos meses* antes de que termine el semestre, para aplicar al siguiente.\n"
    "5) Una vez compres el PIN, se procederá con el *estudio de reintegro*. De ser aprobado, debes acercarte a la *Coordinación* "
    "o a la *Secretaría Académica* para la generación del recibo de matrícula."
)
# (Sin QR de Admisiones; requerido por el documento)

R3 = (
    "*Inscripción / Cancelación de asignaturas*\n\n"
    "📅 *Según el cronograma académico*:\n\n"
    "✅ *Primera semana del semestre:*\n"
    "• Puedes hacer *cancelaciones o inscripciones* directamente ante el *Proyecto Curricular*.\n\n"
     "📧 *Adiciones/Cancelaciones por correo:* envía a *ingelectronica@udistrital.edu.co* el *formato de adiciones y cancelación*.\n"
    "🕒 *Desde la semana 2 en adelante:*\n"
    "• El trámite debe hacerse ante el *Consejo de Facultad*.\n\n"
    "📌 Es muy importante estar pendiente del *cronograma académico oficial*, donde están las fechas exactas.\n\n"
    "📧 *Enviar a Secretaría Académica (carta de cancelacion con motivo, debe ir firmada):* *secing@udistrital.edu.co*, *asecing@udistrital.edu.co*, *sec-secing@udistrital.edu.co*."
)

R4 = (
    "*Trabajo de grado*\n\n"
    "📥 *Toda la información está en la página del Proyecto de Ingeniería Electrónica.*\n"
    f"📄 *Banner* (pasos y requisitos): {TG_BANNER}\n\n"
    "🗓️ *Acta de sustentación:* se solicita con *3 días de anticipación* en el siguiente enlace:\n"
    f"• {TG_FORM_1}\n\n"
    "🗃️ *Permiso para RIUD:* diligencia este formulario *una vez inscrito en RIUD*:\n"
    f"• {TG_FORM_3}\n"
    f"• Guía RIUD (manual): {RIUD_GUIA}\n\n"
   
)
# (Sin QR en esta sección; requerido por el documento. Se eliminaron TG_FORM_2 y TG_FORM_4 de la lista de TG)

R5 = (
    "*Práctica empresarial*\n\n"
    "Las solicitudes se realizan mediante el formulario:\n"
    f"• {TG_FORM_4}\n\n"
    "Procedimiento:\n"
    "1) Solicitar *carta de presentación* (en el mismo formulario) y anexar el *formato*:\n"
    f"   {PE_FORMATO_SOLIC}\n"
    "2) La empresa remite las *funciones*.\n"
    "3) La *Coordinación* responde con la *viabilidad* de las funciones.\n"
    "4) Formaliza la *inscripción* (por el mismo formulario) adjuntando:\n"
    "   • Correo de *Carta de presentación*\n"
    "   • Correo de *Carta de Viabilidad*\n"
    "   • *Contrato*\n"
    "   • *ARL*\n"
    f"   • *Carta del tutor docente de planta*: {PE_CARTA_TUTOR}\n\n"
    f"📄 *Formato de informe de práctica:* {PE_INFORME}"
)

R6 = (
    "*Actas de consejo*\n\n"
    "Las *actas del Consejo de Carrera* se encuentran en:\n"
    "https://udistritaleduco-my.sharepoint.com/:f:/g/personal/ingelectronica_udistrital_edu_co/EsujtjzdgqRCp4ASFiJnFd8BNDaQsDr9hECkqVjtWPzBOA?e=cZGo8t"
)
# (Contenido y título ajustados; antes era “Actas de sustentación”)

R7 = (
    "*Constancias de estudio / Certificados de notas*\n\n"
    "1) 📄 Consulta primero los *valores* en el PDF de *Derechos pecuniarios*:\n"
    "👉 {LINK_DERECHOS}\n\n"
    "2) 💳 Realiza el *pago*: por *PSE* si tienes *Cóndor* activo, o por *banco* si no tienes Cóndor activo.\n\n"
    "3) 📧 Luego envía un *correo* a:\n"
        "3.1) 📧 Si es un certificado de Notas *enviar correo* a:\n"
             "*sec-secing@udistrital.edu.co*\n\n"
        "3.2) 📧 Si es un certificado de Contenidos *enviar correo* a:\n"
             "*secingelectronica@udistrital.edu.co*\n\n"
        "3.3) 📧 Si es una constancia de estudio especial *enviar correo* a:\n"
             "*secingelectronica@udistrital.edu.co*\n\n"
        "3.4) 📧 Si es un certificado de ranking *enviar correo* a:\n"
             "*ingelectronica@udistrital.edu.co*\n\n"
        "3.5) 📧 Si es una constancia de estudio especial *se genera automaticamente* a:\n"
             "*En la misma seccion donde lo pago en el SGA*\n\n"
    "*Incluye:*\n"
    "• Nombre completo\n"
    "• Número de documento\n"
    "• Código estudiantil\n"
    "• Programa académico\n"
)
# (Sin enviar QR adicional aquí; el link ya está en el texto)

R8 = (
    "*Modelo de correo al programa*\n\n"
    "*Asunto:* Solicitud de información sobre trámite académico\n\n"
    "Respetados(as) señores(as),\n\n"
    "Cordial saludo. Me permito solicitar información sobre [describa su caso]. "
    "Quedo atento(a) a los requisitos adicionales que sean necesarios.\n\n"
    "Atentamente,\n[Nombre completo]\n[Documento]\n[Código]\n[Programa: Ingeniería Electrónica]\nCorreo: [su correo]\nTel.: [su número]\n\n"
    "*Destinatario sugerido:* *ingelectronica@udistrital.edu.co*"
)

# ========= WEBHOOKS =========
@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "forbidden", 403

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True, silent=True) or {}

##-------------------------------------------------------------------------------PRUEBAS-----------------------------------------------------
#from threading import Thread
#    Thread(target=process_webhook, args=(data,)).start()
#    return "ok", 200

#def process_webhook(data):

##--------------------------------------------------------------------------------PRUEBAS------------------------------------------------------
    
    try:
        entry  = data["entry"][0]
        change = entry["changes"][0]["value"]
        phone_number_id = change["metadata"]["phone_number_id"]
        messages = change.get("messages", [])
        if not messages:
            return "no messages", 200

        msg = messages[0]
        from_wa = msg["from"]

        body = ""
        if msg.get("type") == "text":
            body = msg["text"].get("body", "").strip().lower()
        elif msg.get("type") == "interactive":
            inter = msg["interactive"]
            if inter.get("type") == "button_reply":
                body = inter["button_reply"]["id"].strip().lower()
            elif inter.get("type") == "list_reply":
                body = inter["list_reply"]["id"].strip().lower()

        # ===== ROUTING =====
        if body in ("hola", "menu", "hi", "buenas"):
            send_welcome(phone_number_id, from_wa)   # logo SOLO aquí
            send_menu_buttons_all(phone_number_id, from_wa)

        elif body == "op_1":
            # Cancelación/Aplazamiento (agregados paz y salvo y carta firmada)
            send_text(phone_number_id, from_wa, R1)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_2":
            # Reintegro (SIN QR; agregado punto 5)
            send_text(phone_number_id, from_wa, R2)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_3":
            # Asignaturas (agregados correos y formato)
            send_text(phone_number_id, from_wa, R3)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_4":
            # Trabajo de grado (sin QR, enlaces ajustados)
            send_text(phone_number_id, from_wa, R4)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_5":
            # Práctica empresarial (reemplaza RIUD)
            send_text(phone_number_id, from_wa, R5)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_6":
            # Actas de consejo (contenido/URL específicos)
            send_text(phone_number_id, from_wa, R6)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_7":
            # Constancias/Notas (sin QR extra)
            send_text(phone_number_id, from_wa, R7)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_8":
            send_text(phone_number_id, from_wa, R8)
            send_back_to_menu_button(phone_number_id, from_wa)

        elif body == "op_9":
            # Paz y salvos (sin QR; se envían solo enlaces en texto)
            texto_paz = (
                "*Paz y salvos*\n\n"
                f"• Laboratorios: {LINK_LABS}\n"
                f"• Biblioteca: {LINK_BIBLIO}\n"
                f"• Bienestar: {LINK_BIENESTAR}"
            )
            send_text(phone_number_id, from_wa, texto_paz)
            send_back_to_menu_button(phone_number_id, from_wa)

        else:
            send_welcome(phone_number_id, from_wa)
            send_menu_buttons_all(phone_number_id, from_wa)

    except Exception as e:
        print("Error procesando payload:", e)
    return "ok", 200    #-------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
