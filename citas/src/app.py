import streamlit as st
from streamlit_option_menu import option_menu
from enviar_email import send
from google_sheets import GoogleSheets
import re #usar expresiones regulares
import uuid
from google_calendar import GoogleCalendar
import numpy as np
import datetime as dt

page_title="Santos Atagualpa"
page_icon="🏥"
layout="centered"

#horas
horas = ["08:00","09:00","10:00","11:00","12:00","15:00","16:00","17:00","18:00","19:00"]
doctores=["Doc. House","Doc. Diana","Doc. Dani","Doc. Sofia"]

document = "Gestion_Citas"
sheet = "citas"
credentials=st.secrets["google"]["credentials_google"]
idcalendar = "willykenneth.alcala@gmail.com"
idcalendar2 = "458a68a459724c22c5a7c01f070f6886671a800bcd08ac29bffd7e32e6e7d37f@group.calendar.google.com"
time_zone = "Europe/Madrid"
#funciones
#validar el formato de email

def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$' #partron para confirmar
    if re.match(patron, email):
        return True
    else:
        return False 

def generar_uid():
    return str(uuid.uuid4())

def add_hours_and_half(time):
    parsed_time=dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time)+dt.timedelta(hours=1, minutes=00)).time()
    return new_time.strftime("%H:%M")


#configuramos la página
st.set_page_config(page_title=page_title,page_icon=page_icon, layout=layout)
#diseño de la aplicacion 

#mostrar imagen
st.image("assets/clinica.jpg", width=700)
#titulo
st.title("Clínica Santos Atagualpa")
st.text("calle Manuel Prada 1568")
#menu opcion
selected=option_menu(menu_title=None, options=["Reservar","Doctores","Detalles"],
            icons=["calendar-date","people","clipboard-minus"],
            orientation="horizontal")


if selected =="Detalles":
    st.subheader("Ubicación: ")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d691.7567113904028!2d-74.63605308388807!3d-11.249136415227756!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1ses-419!2spe!4v1717386792280!5m2!1ses-419!2spe" width="700" height="350" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""",unsafe_allow_html=True)
    #st.image("assets/map.jpg")
    #st.markdown("pula [aquí](https://www.google.com/maps/place/ROUP-Amor+Eterno/@-11.2380067,-74.6388694,19z/data=!4m6!3m5!1s0x910bc1aa60c2b9d9:0xf8d13cc1774a6cda!8m2!3d-11.2380067!4d-74.6383871!16s%2Fg%2F11v64zn3fp?hl=es-419&entry=ttu) para ver la dirección")

    st.subheader("Horarios")
    dia, hora=st.columns(2)

    dia.text("Lunes")
    hora.text("8:00 a.m - 20:00 p.m")
    dia.text("Martes")
    hora.text("8:00 a.m - 20:00 p.m")
    dia.text("Miércoles")
    hora.text("8:00 a.m - 20:00 p.m")
    dia.text("Jueves")
    hora.text("8:00 a.m - 20:00 p.m")
    dia.text("Viernes")
    hora.text("8:00 a.m - 20:00 p.m")
    dia.text("Sábado")
    hora.text("8:00 a.m - 13:00 p.m")

    st.subheader("Contacto")
    st.text("📞 956985623")
    st.subheader("Redes Sociales")

if selected == "Doctores":

    # st.image("assets/doctores.jpg", caption="Nuestros Doctores")
    st.header("Nuestros Doctores: ")
    c1,c2 = st.columns(2)
    c1.image("assets/house.jpg",use_column_width=True)
    c2.image("assets/doc2.jpeg",use_column_width=True)
    c1.image("assets/doc1.jpeg",use_column_width=True)
    c2.image("assets/doc3.jpeg",use_column_width=True)

if selected == "Reservar":
    st.subheader("Reservar")

    c1,c2 = st.columns(2)
    #c1.text_input("Tu nombre*", placeholder="Nombre", label_visibility="hidden") #para ocultar
    nombre = c1.text_input("Tu nombre*")
    celular = c1.text_input("Celular*")
    email = c2.text_input("Tu email*")
    fecha = c2.date_input("Fecha")
    doctor = c1.selectbox("Doctores",doctores)
    if fecha:
        if doctor == "Doc. House":
            id = idcalendar
        elif doctor == "Doc. Diana":
            id = idcalendar2

        calendar = GoogleCalendar(credentials,id)
        hours_blocked = calendar.get_event_start_time(str(fecha))
        result_hours = np.setdiff1d(horas, hours_blocked)
    
    hora = c1.selectbox("Hora",result_hours)
    nota = c2.text_area("Notas")

    enviar = st.button("Reservar")

    #Backend
    if enviar:
        with st.spinner("cargando..."):
            if nombre == "":
                st.warning("El nombre es obligatorio")
            elif celular =="":
                st.warning("El celular es obligatorio")
            elif email =="":
                st.warning("El email es obligatorio")
            elif not validar_email(email):
                st.warning("El email no es válido")
            else:
                #crear evento en google calendar
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour
                munites1 = parsed_time.minute
                end_hours = add_hours_and_half(hora)    
                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                munites2 = parsed_time2.minute
                start_time = dt.datetime(fecha.year,fecha.month,fecha.day,  hours1+2, munites1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                end_time = dt.datetime(fecha.year,fecha.month,fecha.day,  hours2+2, munites2).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

                calendar = GoogleCalendar(credentials,id)
                calendar.create_event(nombre,start_time,end_time,time_zone)
                #crear registro en google sheet
                uid = generar_uid()
                data=[[nombre,email,doctor,str(fecha),hora,nota,celular,uid]]
                gs = GoogleSheets(credentials,document,sheet)
                range= gs.escribir_untimaFila()
                gs.escribir_dato(range,data)
                #enviar email al usuario
                send(email, nombre, fecha, hora, doctor)
                st.success("Su Cita ha sido reservada de forma exitosa.")