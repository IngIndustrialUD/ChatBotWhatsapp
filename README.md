# ChatBotWhatsapp
Código de consumo de API de Whatsapp

1) Variables de entorno en Render
   
VERIFY_TOKEN: cadena que eliges para verificar el webhook (también la pones en Meta).

WHATSAPP_TOKEN: Access Token de la app en Meta (usa de larga duración para producción)

WHATSAPP_API_VERSION (opcional): por defecto v20.0.

3) Deploy en Render (pasos rápidos)
Sube este repo a GitHub.
En Render: New + → Web Service.
Conecta tu repo, elige región, plan Free.
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --workers 2 --threads 4 --timeout 120
Agrega en Environment las variables VERIFY_TOKEN y WHATSAPP_TOKEN.
Deploy. Copia la URL resultante, por ejemplo: https://tu-servicio.onrender.com.

5) Conectar Webhook en Meta Developers
En la app de WhatsApp (Meta Developers) → Configuration → Webhooks:

Callback URL: https://tu-servicio.onrender.com/webhook
Verify Token: el mismo VERIFY_TOKEN
Activa el campo messages en Webhooks Subscriptions.

4) Probar
Escribe “hola” al número de prueba / número oficial vinculado a tu app. Deberías recibir el menú con las 8 opciones y respuestas condicionales.

5) Local (opcional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export VERIFY_TOKEN=mi_token
export WHATSAPP_TOKEN=EAAG...
python app.py
Para exposiciones locales usa ngrok http 5000 y configura esa URL temporal en Meta.

