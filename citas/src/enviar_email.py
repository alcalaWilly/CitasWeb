import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

#funciones
def send(email, nombre, fecha, hora, doctor):
    #credenciales
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]

    sender_email = "Clinica Santos Atagualpa"
    #configurando el servidor
    msg = MIMEMultipart()
    smptp_server = "smtp.gmail.com"
    smtp_port = 587

    #parámetros del mensaje
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject']= "Reserva de Sita"
    #cuerpo del mensaje
    message = f"""  
    Hola {nombre},
    Su Cita ha sido reservada con éxito.
    Fecha: {fecha}
    Hora: {hora}
    Doctor: {doctor}

    Gracias por Elegirnos. 
    Le esperamos, Saludos cordiales.
    """
    #sis e quiere dar estilor en ves de plain es el html
    msg.attach(MIMEText(message,'plain', 'utf-8'))

    #conexion al servidor
    try:
        server = smtplib.SMTP(smptp_server,smtp_port)
        server.starttls() #inicializa
        server.login(user,password) #logeo
        server.sendmail(sender_email, email,msg.as_string())
        server.quit()
        
    except smtplib.SMTPException as e:
        st.exception("Error al eviar email.")