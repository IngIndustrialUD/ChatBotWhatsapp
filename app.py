import os
import requests
from urllib.parse import quote_plus
from flask import Flask, request
from flask import send_from_directory
app = Flask(__name__)

@app.get("/privacy.html")
def privacy():
    return send_from_directory(".", "privacy.html")

# ========= CONFIG =========
VERIFY_TOKEN   = os.getenv("VERIFY_TOKEN", "mi_token_de_verificacion")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "REEMPLAZA_CON_TU_TOKEN")
API_VERSION    = os.getenv("WHATSAPP_API_VERSION", "v22.0")

# Logo
LOGO_URL_UD = os.getenv("LOGO_URL_UD", "")

# Infografías
INFO_CANCELARAPLAZAR = os.getenv("INFO_CANCELARAPLAZAR", "")
INFO_CERTNOTAS       = os.getenv("INFO_CERTNOTAS", "")
INFO_DERECHOS        = os.getenv("INFO_DERECHOS", "")
INFO_CERTESTUDIOSU   = os.getenv("INFO_CERTESTUDIOSU", "")
INFO_CERTESTUDIOSD   = os.getenv("INFO_CERTESTUDIOSD", "")
INFO_PASANTIA        = os.getenv("INFO_PASANTIA", "")

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
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}&data={quote_plus(data)}"

# ========= BIENVENIDA =========
BIENVENIDA = (
    "*Chat Institucional*\n"
    "*Proyecto Curricular de Ingeniería Industrial*\n"
    "*Universidad Distrital Francisco José de Caldas*"
)

def send_welcome(phone_number_id: str, to: str):
    if LOGO_URL_UD:
        send_image_with_caption(phone_number_id, to, LOGO_URL_UD, BIENVENIDA)
    else:
        send_text(phone_number_id, to, BIENVENIDA)

# ========= BOTONES DE NAVEGACIÓN =========
def send_back_tramites(phone_number_id: str, to: str):
    """Botón doble: volver a Trámites O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_tramites", "title": "Volver a Trámites"}},
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )




def send_back_informacion(phone_number_id: str, to: str):
    """Botón doble: volver a Información O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_informacion", "title": "Volver a Información"}},
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )

def send_back_concar(phone_number_id: str, to: str):
    """Botón doble: volver a Consejo de carrera O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_concar", "title": "Consejo de Carrera"}},
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )

def send_back_tragrado(phone_number_id: str, to: str):
    """Botón doble: volver a Trabajo de grado O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_tragrado", "title": "Trabajo de grado"}},
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )



def send_back_otros(phone_number_id: str, to: str):
    """Botón doble: volver a Información O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_informacion", "title": "Volver a Otros"}},
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )



def send_back_to_menu_principal(phone_number_id: str, to: str):
    """Botón simple: solo volver al menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Desea volver al menú principal?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_principal", "title": "Menú principal"}}
        ],
        footer_text=""
    )

# ========= MENÚ PRINCIPAL =========
def send_menu_principal(phone_number_id: str, to: str):
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Menú Principal*\nEn esta sección encontrarás:\n\n*• Tramites:* Derechos pecuniarios, Certificados, Práctica empresarial y contenidos programáticos.\n\n*• Información:* Consejo de carrera, Cancelar/aplazar semestre/asignatura, reintegro, calendario académico, paz y salvos.\n\n*• Otros:* Ceremonias de grado, inscripción Saber Pro, Contactos, Cambio de Plan de estudios, Cambio TI *->* CC.\n\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_tramites",   "title": "Trámites"}},
            {"type": "reply", "reply": {"id": "menu_informacion","title": "Información"}},
            {"type": "reply", "reply": {"id": "menu_otros",      "title": "Otros"}}
        ],
        footer_text=""
    )

# ========= SUBMENÚ TRÁMITES =========
def send_menu_tramites(phone_number_id: str, to: str):
    # Tarjeta 1 de trámites
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Trámites (1/2)*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_derechos",  "title": "Derechos pecuniarios"}},
            {"type": "reply", "reply": {"id": "op_certnotas", "title": "Certificado de notas"}},
            {"type": "reply", "reply": {"id": "op_certest",   "title": "Cert. de estudio"}}
        ],
        footer_text=""
    )
    # Tarjeta 2 de trámites
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Trámites (2/2)*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_practica",  "title": "Práctica empresarial"}},
            {"type": "reply", "reply": {"id": "op_contpro",   "title": "Contenidos programá."}},
            {"type": "reply", "reply": {"id": "menu_principal","title": "Menú principal"}}
        ],
        footer_text=""
    )

# ========= SUBMENÚ INFORMACIÓN (por completar) =========
def send_menu_informacion(phone_number_id: str, to: str):
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Información (1/2)*\nEn esta sección encontrarás:\n\n*• Consejo de Carrera:* Trabajo de grado, homologaciones, actas de consejo.\n\n*• Cancelar/aplazar semestre*\n\n*• Cancelar/Aplazar asignaturas*\n\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_concar", "title": "Consejo de Carrera"}},
            {"type": "reply", "reply": {"id": "op_cancelars", "title":  "Cancelar/aplazar S"}},
            {"type": "reply", "reply": {"id": "op_cancelara","title": "Cancelar/aplazar A"}}
        ],
        footer_text=""
    )
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Información (2/2)*\nEn esta sección encontrarás:\n\n*• Reintegro*\n\n*• Calendario académico*\n\n*• Paz y salvos*\n\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_reintegro",  "title": "Reintegro"}},
            {"type": "reply", "reply": {"id": "op_calend",   "title": "Calendario académico"}},
            {"type": "reply", "reply": {"id": "op_pazsalvos","title": "Paz y Salvos"}}
        ],
        footer_text=""
    )
    button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?\n",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_principal",  "title": "Menú principal"}},
        ],
        footer_text=""
    )

# ========= SUBMENÚ CONSEJO DE CARRERA ==========
def send_menu_concar(phone_number_id: str, to: str):
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Consejo de Carrera*\nEn esta sección encontrarás:\n\n*• Trabajo de grado:* Modalidades de grado\n\n*• Información procesos proyecto de grado*\n\n*• Formulario del RIUD*\n\n Seleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_tragrado",   "title": "Trabajo de grado"}},
            {"type": "reply", "reply": {"id": "op_homo",   "title": "Homologaciones"}},
            {"type": "reply", "reply": {"id": "op_actconsejo","title": "Actas de Consejo"}}
        ],
        footer_text=""
    )
    button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?\n",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_informacion",  "title": "Información"}},
            {"type": "reply", "reply": {"id": "menu_principal",  "title": "Menú principal"}},
        ],
        footer_text=""
    )

# ========= SUBMENÚ TRABAJO DE GRADO ==========
def send_menu_tragrado(phone_number_id: str, to: str):
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Consejo de Carrera*\nEn esta sección encontrarás:\n\n*• Trabajo de grado:* Modalidades de grado\n\n*• Información procesos proyecto de grado*\n\n*• Formulario del RIUD*\n\n Seleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_modgrado",   "title": "Modalidades grado"}},
            {"type": "reply", "reply": {"id": "op_seggrado",   "title": "Seguimiento grado"}},
            {"type": "reply", "reply": {"id": "op_formriud","title": "Formulario RIUD"}}
        ],
        footer_text=""
    )
    button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?\n",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_concar",  "title": "Consejo de Carrera"}},
            {"type": "reply", "reply": {"id": "menu_principal",  "title": "Menú principal"}},
        ],
        footer_text=""
    )





# ========= SUBMENÚ OTROS (por completar) =========
def send_menu_otros(phone_number_id: str, to: str):
    button_message(
        phone_number_id, to,
        header=None,
        body_text="*Otros*\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "op_otros_1",   "title": "Opción 1"}},
            {"type": "reply", "reply": {"id": "op_otros_2",   "title": "Opción 2"}},
            {"type": "reply", "reply": {"id": "menu_principal","title": "⬅️ Menú principal"}}
        ],
        footer_text=""
    )

# ========= LINKS =========
LINK_DERECHOS   = "https://youtu.be/jbuQmmPCJ2E"
LINK_SECACADEMICA = "asecing@udistrital.edu.co"
LINK_LABS = "https://facingenieria.udistrital.edu.co/laboratorios/labing/index.php/tramites-y-servicios/paz-y-salvo"
LINK_BIBLIO     = "https://bibliotecas.udistrital.edu.co/servicios/paz_y_salvos"
LINK_BIENESTAR  = "https://bienestar.udistrital.edu.co/node/634"




LINK_RIUD       = "https://repositorio.udistrital.edu.co"
LINK_ADMISIONES = "https://www.udistrital.edu.co/admisiones/index.php/"
TG_FORM_1       = "https://forms.office.com/r/8ZkpzjTYvX"
TG_FORM_3       = "https://forms.office.com/r/0r0hjX0Bh4"
TG_FORM_4       = "https://forms.office.com/r/P81G4Fqt0A"
TG_BANNER       = "https://udistritaleduco-my.sharepoint.com/:b:/g/personal/ingelectronica_udistrital_edu_co/EQRfFbhqDKlPsIdKzjKL_HsBkYzq5JBC7PBkqlxDFU0TFQ?e=MXNNwn"
RIUD_GUIA       = "https://repository.udistrital.edu.co/assets/custom/docs/Guia_RIUD_autor.pdf"
PE_FORMATO_SOLIC= "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/EeGl6EoBDpJNuxKg6PqYJrwBZhx6TYivnL7uRWKco_D_LA?e=ig9DQu"
PE_CARTA_TUTOR  = "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/EXp2Pl4gjFBDoIksXo_7_dYBwh8z_V6KO4D466Jr9A6biw?e=DboPOo"
PE_INFORME      = "https://udistritaleduco-my.sharepoint.com/:w:/g/personal/ingelectronica_udistrital_edu_co/Ea6rADiXua9FjuiE6B0ViGsBJ-Kc217eO1-9e-4LpS0hMw?e=IJ27L3"

# ========= RESPUESTAS =========
R_DERECHOS = (
    "*Derechos pecuniarios*\n\n"
    "Ingresa al siguiente enlace para conocer el paso a paso para que solicites tus documentos "
    "sin errores desde el Sistema de Gestión Académica\n"
    f"Enlace: *{LINK_DERECHOS}*\n\n"
    "Dentro de los derechos pecuniarios encontrarás los siguientes servicios disponibles:\n"
    "• Constancia de estudio\n"
    "• Constancia de estudio especial\n"
    "• Certificado de notas\n"
    "⚠️ Revisa muy bien el procedimiento para evitar complicaciones."
)

R_CERTNOTAS = (
    "👉 *Cómo generar tu certificado de notas paso a paso*\n\n"
    "*Paso 1:* Ingresa a SGA con tus datos personales.\n"
    "*Paso 2:* Menú superior izquierdo → Servicios → Derechos pecuniarios → Generar recibo\n"
    "*Paso 3:* En la lista desplegable elige *'Certificado de Notas'* y haz clic en *Aceptar*\n\n"
    "*IMPORTANTE:* Verifica que tus datos personales estén correctos antes de generar el recibo\n\n"
    "*Paso 4:* Luego de haber pagado en línea con PSE, podrás descargar en *'Recibos generados'* el certificado\n\n"
    "Por último, si deseas incluir información adicional necesaria, envía el PDF del certificado al correo: "
    "*sec-seing@udistrital.edu.co*\n"
    "El proceso puede tardar entre 1 y 3 días hábiles."
)

R_CERTEST_1 = (
    "*Cómo generar tu certificado de estudios normal. Paso a paso:*\n\n"
    "*Paso 1:* Entra al portal institucional con tu *usuario*\n"
    "*Paso 2:* En el menú izquierdo: Servicios → Derechos pecuniarios → Generar recibo\n"
    "*Paso 3:* En el campo Derecho pecuniario, elige *'Constancias de estudio'* y haz clic en Aceptar\n"
    "Nota: Una vez hecho esto, se generará el recibo de pago automáticamente\n"
    "*Paso 4:* Elige pago en línea PSE → Selecciona tu banco → Completa la transacción\n"
)

R_CERTEST_2 = (
    "*Certificado de estudios especial. Paso a paso:*\n\n"
    "*Paso 1:* Primero genera y paga el recibo como en el proceso de Certificado de estudios normal.\n"
    "*Paso 2:* Envía un correo a: *secingindustrial@udistrital.edu.co* incluyendo:\n"
    "• Nombre completo\n"
    "• Código estudiantil\n"
    "• Tipo y número de documento\n"
    "• Ciudad de expedición\n"
    "• Número de contacto\n\n"
    "Nota: Especifica el tipo de *certificado*\n\n"
    "*Paso 3:* La constancia será enviada al correo del solicitante dentro de los "
    "*tres días hábiles siguientes*."
)

R_PRACTICA = (
    "*Práctica empresarial*\n\n"
)

R_cancelars = (
    "*Como cancelar o aplazar semestre*\n\n"
    "Ten en cuenta de que existen 2 momentos diferentes para solicitar o"
    "el aplazamiento del semestre\n\n"
    "• *Durante los primero 10 días hábiles de clase:*\n"
    "Sistema de Gestión Académica *->* Servicios *->* Retiro voluntario.\n"
    "Diligenciar el *formulario* para realizar la solicitud\n\n"
    "• *Después de las 2 semanas iniciadas clases:*\n"
    "Debes realizar la solicitud a *Consejo de Facultad - Secretaría Académica*, al correo:\n\n"
    f"*{LINK_SECACADEMICA}*\n\n"
    "• *En ambos casos:* Debes enviar la carta de solicitud firmada explicando los motivos,\n"
    "además de los Paz y Salvos de:\n\n"
    f"• *Laboratorios:* {LINK_LABS}\n"
    f"• *Biblioteca:* {LINK_BIBLIO}\n"
    f"• *Bienestar institucional:* {LINK_BIENESTAR}\n"
    "*- Reintegro posterior:* Tras la aprobación del *aplazamiento* o *cancelación* el\n\n"
    "estudiante tiene máximo dos períodos académicos para solicitar reintegro"
)

R_tragrado = (
    "En proceso, muy amable"
)

R_homo = (
    "En proceso, muy amable"
)

R_actconsejo = (
    "En proceso, muy amable"
)

R_modgrado = (
    "En proceso, muy amable"
)

R_seggrado = (
    "En proceso, muy amable"
)

R_formriud = (
    "En proceso, muy amable"
)

# ========= WEBHOOKS =========
@app.get("/webhook")
def verify():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "forbidden", 403

processed_ids = set()

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    from threading import Thread
    Thread(target=process_webhook, args=(data,)).start()
    return "ok", 200

def process_webhook(data):
    try:
        entry           = data["entry"][0]
        change          = entry["changes"][0]["value"]
        phone_number_id = change["metadata"]["phone_number_id"]
        messages        = change.get("messages", [])
        if not messages:
            return

        msg    = messages[0]
        msg_id = msg.get("id", "")
        if msg_id in processed_ids:
            print(f"Duplicado ignorado: {msg_id}")
            return
        processed_ids.add(msg_id)

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

        # ===== SALUDO INICIAL =====
        if body in ("hola", "menu", "hi", "buenas", "menu_principal"):
            send_welcome(phone_number_id, from_wa)
            send_menu_principal(phone_number_id, from_wa)

        # ===== EASTER EGG =====
        elif body in ("Como estas", "Cómo estás", "¿Cómo estás?", "Como estás",
                      "Cómo estas", "¿Como estas?", "¿como estás?"):
            SALUDO = (
                "*Nadie se había preocupado tanto por mí* 🥹\n"
                "Ahí vamos, luchandola\n"
                "Muchas gracias por preguntar"
            )
            send_text(phone_number_id, from_wa, SALUDO)
            send_back_to_menu_principal(phone_number_id, from_wa)

        # ===== MENÚS PRINCIPALES =====
        elif body == "menu_tramites":
            send_menu_tramites(phone_number_id, from_wa)

        elif body == "menu_informacion":
            send_menu_informacion(phone_number_id, from_wa)

        elif body == "menu_otros":
            send_menu_otros(phone_number_id, from_wa)
    
        elif body == "menu_concar":
            send_menu_concar(phone_number_id, from_wa)

        elif body == "menu_tragrado":
            send_menu_tragrado(phone_number_id, from_wa)
        
        # ===== OPCIONES DE TRÁMITES =====
        elif body == "op_derechos":
            send_image_with_caption(phone_number_id, from_wa, INFO_DERECHOS, "")
            send_text(phone_number_id, from_wa, R_DERECHOS)
            send_back_tramites(phone_number_id, from_wa)

        elif body == "op_certnotas":
            send_image_with_caption(phone_number_id, from_wa, INFO_CERTNOTAS, "")
            send_text(phone_number_id, from_wa, R_CERTNOTAS)
            send_back_tramites(phone_number_id, from_wa)

        elif body == "op_certest":
            send_image_with_caption(phone_number_id, from_wa, INFO_CERTESTUDIOSU, "")
            send_text(phone_number_id, from_wa, R_CERTEST_1)
            send_image_with_caption(phone_number_id, from_wa, INFO_CERTESTUDIOSD, "")
            send_text(phone_number_id, from_wa, R_CERTEST_2)
            send_back_tramites(phone_number_id, from_wa)

        elif body == "op_practica":
            send_image_with_caption(phone_number_id, from_wa, INFO_PASANTIA, "")
            send_text(phone_number_id, from_wa, R_PRACTICA)
            send_back_tramites(phone_number_id, from_wa)

        elif body == "op_contpro":
            send_text(phone_number_id, from_wa, "⚙️ Contenidos programáticos — próximamente.")
            send_back_tramites(phone_number_id, from_wa)

        # ===== OPCIONES DE INFORMACIÓN (por completar) =====
        elif body == "op_cancelara":
            #Cancelar/Aplazar de asignaturas 
            send_text(phone_number_id, from_wa, "Cancelar asignatura - Próximamente")
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_cancelars":
            #Cancelar/Aplazar de semestre 
            send_image_with_caption(phone_number_id, from_wa, INFO_CANCELARAPLAZAR, "")
            send_text(phone_number_id, from_wa, R_cancelars)
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_reintegro":
            #Cancelar/Aplazar de semestre 
            send_text(phone_number_id, from_wa, "Reintegro - Próximamente")
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_calend":
            #Cancelar/Aplazar de semestre 
            send_text(phone_number_id, from_wa, "Calendario académico - Próximamente")
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_pazsalvos":
            #Cancelar/Aplazar de semestre 
            send_text(phone_number_id, from_wa, "Paz y Salvos - Próximamente")
            send_back_informacion(phone_number_id, from_wa)


        # ===== OPCIONES DE CONSEJO DE CARRERA =====
        elif body == "op_tragrado":
            #Trabajo de grado
            send_text(phone_number_id, from_wa, R_tragrado)
            send_back_concar(phone_number_id, from_wa)

        elif body == "op_homo":
            #Homologaciones
            send_text(phone_number_id, from_wa, R_homo)
            send_back_concar(phone_number_id, from_wa)

        elif body == "op_actconsejo":
            #Actas de Consejo
            send_text(phone_number_id, from_wa, R_actconsejo)
            send_back_concar(phone_number_id, from_wa)

        # ===== OPCIONES DE TRABAJO DE GRADO =====
        elif body == "op_modgrado":
            #Actas de Consejo
            send_text(phone_number_id, from_wa, R_modgrado)
            send_back_tragrado(phone_number_id, from_wa)
        elif body == "op_seggrado":
            #Actas de Consejo
            send_text(phone_number_id, from_wa, R_seggrado)
            send_back_tragrado(phone_number_id, from_wa)
        elif body == "op_formriud":
            #Actas de Consejo
            send_text(phone_number_id, from_wa, R_formriud)
            send_back_tragrado(phone_number_id, from_wa)


        
        # ===== OPCIONES DE OTROS (por completar) =====
        elif body == "op_otros_1":
            send_text(phone_number_id, from_wa, "Otros opción 1 — por completar.")
            send_back_to_menu_principal(phone_number_id, from_wa)

        elif body == "op_otros_2":
            send_text(phone_number_id, from_wa, "Otros opción 2 — por completar.")
            send_back_to_menu_principal(phone_number_id, from_wa)

        # ===== DEFAULT =====
        else:
            send_welcome(phone_number_id, from_wa)
            send_menu_principal(phone_number_id, from_wa)

    except Exception as e:
        print("Error procesando payload:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
