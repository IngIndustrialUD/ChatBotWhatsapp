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
INFO_PRACTICA        = os.getenv("INFO_PRACTICA", "")
PENSUM = os.getenv("PENSUM", "")
SABERPRO = os.getenv("SABERPRO", "")

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
    """Botón doble: volver a Otros O ir al Menú principal"""
    return button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_otros", "title": "Volver a Otros"}},
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
        body_text="*Información (1/2)*\nEn esta sección encontrarás:\n\n*• Consejo de Carrera:* Trabajo de grado, homologaciones, actas de consejo.\n\n*• Cancelar/aplazar semestre*\n\n*• Adiciones y cancelaciones*\n\nSeleccione una opción:",
        buttons=[
            {"type": "reply", "reply": {"id": "menu_concar", "title": "Consejo de Carrera"}},
            {"type": "reply", "reply": {"id": "op_cancelars", "title":  "Cancelar/aplazar S"}},
            {"type": "reply", "reply": {"id": "op_adcan","title": "Adición/Cancelación"}}
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
        body_text="*Trabajo de grado*\nEn esta sección encontrarás:\n\n*• Modalidades de grado*\n\n*• Seguimiento proyecto de grado*\n\n*• Formulario del RIUD*\n\nSeleccione una opción:",
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
            {"type": "reply", "reply": {"id": "op_cergrado",   "title": "Ceremonias de grado"}},
            {"type": "reply", "reply": {"id": "op_saberpro",   "title": "Inscripción SaberPro"}},
            {"type": "reply", "reply": {"id": "op_contactos","title": "Contactos"}}
        ],
        footer_text=""
    )
    button_message(
        phone_number_id, to,
        header=None,
        body_text="¿Qué deseas hacer ahora?\n",
        buttons=[
            {"type": "reply", "reply": {"id": "op_cambioestudios",  "title": "Cambio Plan estudios"}},
            {"type": "reply", "reply": {"id": "op_actualizardatos",  "title": "Actualizar datos"}},
                {"type": "reply", "reply": {"id": "menu_principal",  "title": "Menú Principal"}}
        ],
        footer_text=""
    )
    
# ========= LINKS =========
LINK_DERECHOS   = "https://youtu.be/jbuQmmPCJ2E"
LINK_SECACADEMICA = "asecing@udistrital.edu.co"
CORREO_SECING = "secing@udistrital.edu.co"
LINK_LABS = "https://facingenieria.udistrital.edu.co/laboratorios/labing/index.php/tramites-y-servicios/paz-y-salvo"
LINK_BIBLIO     = "https://bibliotecas.udistrital.edu.co/servicios/paz_y_salvos"
LINK_BIENESTAR  = "https://bienestar.udistrital.edu.co/node/634"
LINK_HOMO = "https://www.udistrital.edu.co/admisiones/index.php/instructivo/transferencias/consideraciones-generales"
LINK_ACUERDOHOMO = "https://sgral.udistrital.edu.co/xdata/ca/acu_2018-04.pdf"
LINK_ACTASCONSEJO = "https://udistritaleduco-my.sharepoint.com/personal/ingindustrial_udistrital_edu_co/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fingindustrial%5Fudistrital%5Fedu%5Fco%2FDocuments%2FActas%20Consejo%20de%20Carrera%20Ing%2E%20Industrial&ga=1"
LINK_MODGRADO = "https://aulasvirtuales.udistrital.edu.co/mod/forum/view.php?id=259484"
LINK_RIUD       = "https://repository.udistrital.edu.co/assets/custom/docs/Guia_RIUD_autor.pdf "
LINK_ADMISIONES = "https://www.udistrital.edu.co/admisiones/index.php/"
LINK_RESULTADOS = "https://www.udistrital.edu.co/admisiones/index.php/resultados"
LINK_CALENDARIO = "https://www.udistrital.edu.co/nuestra-universidad/informacion-institucional/calendario-academico"
RIUD_FORM = "https://forms.cloud.microsoft/pages/responsepage.aspx?id=74gT1bBqY0OflNVmRKRZcH0jtLlRoRZEhuhTvxVW7PFUMlA2T0NLUllFNDdMVDFYNklMS0M4WlBMOC4u&origin=lprLink&route=shorturl"
LINK_RESCAMBIO = "https://sgral.udistrital.edu.co/xdata/ca/res_2023-074.pdf"
LINK_INFOCAMBIO = "https://facingenieria.udistrital.edu.co/ingindustrial/index.php/publicacion/informacion-nuevo-plan"
LINK_PLANESTUDIOS = "https://facingenieria.udistrital.edu.co/ingindustrial/index.php/node/637"
LINK_DATOSSGA = "https://forms.office.com/pages/responsepage.aspx?id=74gT1bBqY0OflNVmRKRZcMQgTuVxZ_tGj-X185s4oQNUNkNVNU5RUVJRMThRQUFKQ0hDQVQwNjNLWC4u&route=shorturl"
LINK_ICFES = "https://bpms-portal.icfes.gov.co/pqrs"
LINK_CERGRADO = "https://facingenieria.udistrital.edu.co/facultad/secretaria-academica/procesos-cronogramas/ceremonia-de-grado"
FORM_SABERPRO = "https://forms.office.com/pages/responsepage.aspx?id=74gT1bBqY0OflNVmRKRZcNLWaHcsc_lIvTiQtTlPwYtUNTBUQjRLRDdQS0pQOE5XQVo5N0I5U09YRC4u&origin=lprLink&route=shorturl"
FORM_GRADO = "https://forms.office.com/r/nVL5aUuDDA?origin=lprLink"
LINK_PRACTICA = "https://aulasvirtuales.udistrital.edu.co/mod/forum/discuss.php?d=62764#p119885"
FORM_PRACTICA = "https://forms.office.com/pages/responsepage.aspx?id=74gT1bBqY0OflNVmRKRZcH0jtLlRoRZEhuhTvxVW7PFUM1lQVllJTExKVElFR0FZRTA0TDlDRTdKTS4u&origin=lprLink&route=shorturl"

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
    "La información acerca de la práctica empresarial puedes encontrarla a continuación:\n"
    f"{LINK_PRACTICA}"
    "\n\nPara realizar la solicitud de la *práctica empresarial*, diligencia el siguiente formulario:\n"
    f"{FORM_PRACTICA}"
)

R_CONTPRO = (
    "*Contenidos programáticos*\n\n"
    "En el siguiente enlace puedes consultar los contenidos programáticos *(syllabus)* de "
    "cada asignatura del programa.\n\n"
    "Al seleccionar una materia, encontrarás información detallada sobre sus objetivos, temáticas, "
    "metodología y criterios de evaluación:\n"
    f"{LINK_PLANESTUDIOS}"
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

R_homo = (
    "*Homologaciones*\n\n"
    "La información referente a transferencias internas, transferencias externas,"
    "y homologaciones puede encontrarse en el siguiente enlace:\n"
    f"{LINK_HOMO}\n\n"
    "• Es responsabilidad del *estudiante* que solicita la homologación entregar los "
    "contenidos temáticos de las asignaturas o espacios académicos objeto de homologación\n\n"
    "• Solo podrán ser objeto de posibles homologaciones los espacios académicos (asignaturas)"
    " *cursados y aprobados* con nota *igual* o *superior* a 3.5 sobre 5.0, o su equivalente en"
    " una escala diferente\n\nEnlace del *Acuerdo N°04, octubre 16 de 2018:*\n"
    f"{LINK_ACUERDOHOMO}"
)

R_actconsejo = (
    "*Actas de consejo*\n\n"
    "En el siguiente enlace puedes encontrar la publicación de las actas de consejo:\n"
    f"{LINK_ACTASCONSEJO}"
)

R_modgrado = (
    "*Modalidades de grado*\n\nSi deseas saber información sobre las modalidades de grado,"
    f" dirígete al enlace a continuación:{LINK_MODGRADO}"
    "\n\nEn el debate *'Formatos Presentación Modalidades de Grado'* se encuentra el "
    "*Acuerdo No.02 de 2023, procedimiento modalidades de grado.pdf* y más información de interés"
    "\n\nPara iniciar el proceso, dirígete al siguiente formulario:\n"
    f"{FORM_GRADO}"
)

R_seggrado = (
    "*Seguimiento proyecto de grado*\n\n"
    "A continuación encontrarás el formulario para registrar formalmente tu trabajo de "
    "grado y solicitar la asignación de un docente jurado, lo que permite dar inicio al "
    "proceso académico y cumplir con los requisitos establecidos.\n\n"
    "*Si tu modalidad es pasantía, ten en cuenta de que debes realizar el trámite directamente con la oficina de pasantías*\n\n"
    "También puedes consultar información adicional en el siguiente enlace:\n"
    f"{LINK_MODGRADO}\n"
    "En la ruta: *Pregrados -> Facultad de ingeniería -> Ingeniería Industrial -> Área administrativa -> Ingeniería Industrial -> Información Trabajo de Grado*"
)

R_formriud = (
    "Permiso para RIUD:\n Diligencia este formulario una vez inscrito en RIUD:\n\n"
    f" - *{RIUD_FORM}*\n\n"
    "Guia RIUD (manual):\n"
    f"{LINK_RIUD}"
)

R_ADCAN = (
    "*Adiciones y cancelaciones*\n\n"
    "El proceso de adiciones y cancelaciones estará habilitado hasta el *31 de julio de 2026.*\n\n"
    "Por medio del Sistema de Gestión Académica (SGA) los estudiantes podrán *adicionar* y "
    "*cancelar* asignaturas en el horario mencionado anteriormente\n\n"
    "En el caso de cancelar una materia en período extemporáneo, se debe:\n"
    f"*Enviar* solicitud a consejo de facultad por medio del correo:\n {CORREO_SECING}\n"
    "Adjuntando información personal y la razón por la cual desea cancelar."
)


R_REINTEGRO = (
    "*Reintegro*\n\n"
    "*1.* Consulta la programación y requisitos del proceso de admisiones:\n"
    f"{LINK_ADMISIONES}"
    "\n\n*2.* Revisa cuándo se habilita el proceso y los requisitos antes de inscribirte\n\n"
    "*3.* Adquiere el *PIN de reintegro* en las fechas indicadas (es necesario para iniciar la inscripción\n\n"
    "*4.* Genera y paga el recibo de inscripción a través del sistema.\n\n"
    "*5.* Completa el formulario en línea.\n\n"
    "*6.* Descarga e imprime el comprobante de inscripción.\n\n"
    "*7.* Consulta los resultados en:\n"
    f"{LINK_RESULTADOS}"
)

R_CALENDARIO = (
    "*Calendario académico*\n\n"
    "A continuación puedes consultar el calendario académico:\n\n"
    f"*{LINK_CALENDARIO}*"
)

R_PAZSALVOS = (
    "*Paz y Salvos*\n\n"
    "A continuación encontrarás los Paz y Salvos de laboratorios, biblioteca y bienestar institucional:\n\n"
f"• *Laboratorios:* {LINK_LABS}\n\n"
    f"• *Biblioteca:* {LINK_BIBLIO}\n\n"
    f"• *Bienestar institucional:* {LINK_BIENESTAR}\n\n"
)

R_CERGRADO = (
    "*Ceremonias de grado*\n\n"
    "La información referente a ceremonia de grado se podrá encontrar en el siguiente enlace:\n"
    f"{LINK_CERGRADO}"
    "\n\nLa información dispuesta en la página está sujeta a *cronograma* de facultad."
)

R_SABERPRO = (
    "*Examen Saber Pro y T&T*\n\n"
    "Para realizar la inscripción al examen Saber Pro y T&T debes seguir diligenciar el "
    "siguiente formulario:\n"
    f"{FORM_SABERPRO}"
    "\n\nLuego, se debe tener presente los siguientes pasos: \n\n"
    "*1.* Recibir usuario y clave temporal enviado por el ICFES al *correo institucional* o"
    " *correo registrado en Prisma*\n"
    "*2.* Ingresar al aplicativo y completar la información requerida.\n"
    "*3.* Generar la referencia de pago del examen en Prisma\n\n"
    "*Fechas de inscripción:*\n"
    "*- Pago ordinario:* Desde el 13 de abril al 15 de mayo de 2026\n"
    "*- Pago extraordinario:* Desde el 19 de mayo al 12 de junio de 2026\n\n"
    "*Valor examen:*\n"
    "*- Ordinario:* $126.000\n"
    "*- Extraordinario:* $189.000\n\n"
    "Es responsabilidad del estudiante verificar su estado de pago en Prisma\n\n"
    "En caso de tener inconvenientes en el proceso de inscripción, dirígete al siguiente enlace:\n"
    f"{LINK_ICFES}"
    "\nO dirígete directamente a las oficinas de atención del ICFES"
)

R_CONTACTOS = (
    "*Contactos*\n\n"
    "Puedes comunicarte con proyecto curricular de Ingenieria Industrial llamando a:\n"
    "*(+57) 60113239300*\n"
    "Ext - Coordinador: *1514*\n"
    "Ext - Secretaría: *1509*\n\n"
    "O escribiendo por medio de los correos electrónicos:\n"
    "- *secingindustrial@udistrital.edu.co*\n"
    "- *ingindustrial@udistrital.edu.co*\n\n"
    "Nos encontramos en la dirección: *Carrera 7 # 40B - 53 Piso 5*\n\n"
    "Con el siguiente horario:\n"
    "- *Medios Virtuales:* Lunes a Viernes de 10:00 a.m. - 1:00 p.m. y de 2:00 p.m. - 6:00 p.m.\n"
    "- *Atención general:* Lunes a Viernes de 08:00 a.m. a 5:00 p.m."
)

R_CAMBIOESTUDIOS = (
    "*Cambio de Plan de estudios*\n\n"
    "Puedes consultar el cambio de pensum en el siguiente enlace:\n"
    f"{LINK_PLANESTUDIOS}\n\n"
    "*Al seleccionar cada asignatura, podrás acceder al syllabus correspondiente*\n\n"
    "También encontrarás *información del nuevo plan de estudios*, incluyendo la *herramienta en excel* "
    "y el *formato de autorización* para el cambio del plan de estudios, en el "
    "siguiente enlace:\n"
    f"*{LINK_INFOCAMBIO}*\n\n"
    "Por último, puedes revisar la Resolución No. 074 del 04 de diciembre de 2023, "
    "relacionada con el cambio de pensum, aquí: \n"
    f"*{LINK_RESCAMBIO}*"
)

R_CAMBIODATOS = (
    "*Actualizar información personal*\n\n"
    "Para actualizar tu nombre, tipo de documento o número de identificación, debes "
    "diligenciar el siguiente formulario:\n"
    f"*{LINK_DATOSSGA}*\n\n"
    "También puedes acceder a este formulario a través del Sistema de Gestión Académica, "
    "en la ruta:\n\n"
    "*Datos personales → Actualizar datos*"
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
            send_image_with_caption(phone_number_id, from_wa, INFO_PRACTICA, "")
            send_text(phone_number_id, from_wa, R_PRACTICA)
            send_back_tramites(phone_number_id, from_wa)

        elif body == "op_contpro":
            send_image_with_caption(phone_number_id, from_wa, PENSUM, "")
            send_text(phone_number_id, from_wa, R_CONTPRO)
            send_back_tramites(phone_number_id, from_wa)

        # ===== OPCIONES DE INFORMACIÓN (por completar) =====
        elif body == "op_adcan":
            #Cancelar/Aplazar de asignaturas 
            send_text(phone_number_id, from_wa, R_ADCAN)
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_cancelars":
            #Cancelar/Aplazar de semestre 
            send_image_with_caption(phone_number_id, from_wa, INFO_CANCELARAPLAZAR, "")
            send_text(phone_number_id, from_wa, R_cancelars)
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_reintegro":
            #REINTEGRO 
            send_text(phone_number_id, from_wa, R_REINTEGRO)
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_calend":
            #Calendario académico
            send_text(phone_number_id, from_wa, R_CALENDARIO)
            send_back_informacion(phone_number_id, from_wa)
            
        elif body == "op_pazsalvos":
            #PAZ Y SALVOS
            send_text(phone_number_id, from_wa, R_PAZSALVOS)
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
            #send_image_with_caption(phone_number_id, from_wa, BANNERGABRIELA, "")
            send_text(phone_number_id, from_wa, R_seggrado)
            send_back_tragrado(phone_number_id, from_wa)
        elif body == "op_formriud":
            #Actas de Consejo
            send_text(phone_number_id, from_wa, R_formriud)
            send_back_tragrado(phone_number_id, from_wa)


        
        # ===== OPCIONES DE OTROS (por completar) =====
        elif body == "op_cergrado":
            send_text(phone_number_id, from_wa, R_CERGRADO)
            send_back_otros(phone_number_id, from_wa)

        elif body == "op_saberpro":
            send_image_with_caption(phone_number_id, from_wa, SABERPRO, "")
            send_text(phone_number_id, from_wa, R_SABERPRO)
            send_back_otros(phone_number_id, from_wa)

        elif body == "op_contactos":
            send_text(phone_number_id, from_wa, R_CONTACTOS)
            send_back_otros(phone_number_id, from_wa)

        elif body == "op_cambioestudios":
            send_image_with_caption(phone_number_id, from_wa, PENSUM, "")
            send_text(phone_number_id, from_wa, R_CAMBIOESTUDIOS)
            send_back_otros(phone_number_id, from_wa)

        elif body == "op_actualizardatos":
            send_text(phone_number_id, from_wa, R_CAMBIODATOS)
            send_back_otros(phone_number_id, from_wa)

        

        # ===== DEFAULT =====
        else:
            send_welcome(phone_number_id, from_wa)
            send_menu_principal(phone_number_id, from_wa)

    except Exception as e:
        print("Error procesando payload:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
