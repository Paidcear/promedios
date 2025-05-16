#v2 --JCDM
#MEJORAS EN UI
#MEJORAS EN FORMATO PDF

import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(
    page_title="SGPromedios",
    page_icon="logo.png"
)

# Función para calcular el promedio
def calcular_promedio(examen, tareas, actividades, complementos, complemento_extra_examen, complemento_extra_tareas, complemento_extra):
    examen_final = (examen / 12) * 48  + complemento_extra_examen  # Examen con valor total de 48 puntos + puntos extra
    tareas_total = sum(tareas) + complemento_extra_tareas  # Tareas con valor total de 20 puntos + puntos extra
    actividades_total = sum(actividades)
    complementos_total = sum(complementos)

    # Promedio total con complemento extra
    total = examen_final + tareas_total + actividades_total + complementos_total + complemento_extra
    return total, examen_final, tareas_total, actividades_total, complementos_total

# Función para determinar el color del promedio
def determinar_color(promedio):
    if promedio <= 55:
        return 'red'
    elif promedio <= 59:
        return 'darkorange'
    elif promedio <= 100:
        return 'green'
    else:
        return 'darkviolet'

# Función para generar el PDF
def generar_pdf(examen_final, tareas_total, actividades_total, complementos_total, complemento_extra, complemento_extra_examen, complemento_extra_tareas, promedio_final, actividades, id_estudiante):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Agregar el logo
    pdf.image("icom.png", x=10, y=8, w=25)

    # Establecer título
    pdf.set_font('Arial', 'B', 22)
    pdf.cell(190, 5, 'Instituto Comercial México', ln=True, align='C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, 'Desglose de Promedio Final', ln=True, align='C')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 3, 'Individual', ln=True, align='C')
    #pdf.ln(20)
    pdf.image("logo1.png", x=42, y=70, w=120)

    # Agregar contenido al reporte
    pdf.ln(10)  # Espacio
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(190, 10, f"ID del Estudiante: {id_estudiante}", ln=True, align='R')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 7, f"Examen Final (48 puntos)", ln=True)
    pdf.cell(230, 7, f"{examen_final:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(5)
    pdf.cell(200, 7, f"Tareas (20 puntos)", ln=True)
    pdf.cell(230, 7, f"{tareas_total:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(5)
    pdf.cell(200, 7, f"Complementos Cualitativos (20 puntos)", ln=True)
    pdf.cell(230, 7, f"{complementos_total:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(10)  # Espacio adicional
    pdf.cell(200, 10, 'Puntos extra de Tarea y Examen sumados en el total de Examen Final', ln=True)
    pdf.cell(200, 7, f"Portada de la materia (2 puntos)", ln=True)
    pdf.cell(230, 7, f"{complemento_extra:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(5)
    pdf.cell(200, 7, f"Puntaje Extra de Examen (1 punto)", ln=True)
    pdf.cell(230, 7, f"{complemento_extra_examen:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(5)
    pdf.cell(200, 7, f"Puntaje Extra de Tareas (1 punto)", ln=True)
    pdf.cell(230, 7, f"{complemento_extra_tareas:.2f} puntos obtenidos", border=1, ln=True)
    pdf.ln(10)  # Espacio adicional

    pdf.set_font('Arial', 'B', 18)
    pdf.cell(200, 12, f"Promedio Final Total: {promedio_final:.2f} puntos", border=1, ln=True)

    # Desglose de actividades en clase
    pdf.ln(10)  # Espacio adicional
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, "Desglose de Actividades en Clase:", ln=True)

    pdf.set_font('Arial', 'B', 12)
    actividades_desglose = ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Semana 5"]
    for i, actividad in enumerate(actividades_desglose):
        estado = "Asistencia" if actividades[i] == 4 else "Inasistencia"
        pdf.cell(200, 10, f"{actividad}: {estado}", ln=True)

    # Guardar el archivo PDF en un directorio temporal de Streamlit, incluyendo el ID en el nombre
    pdf_dir = os.path.join(os.getcwd(), f"reporte_general_{id_estudiante}.pdf")
    pdf.output(pdf_dir)
    return pdf_dir

# Interfaz de Streamlit
#st.write("**cdelgado**")
st.title("SGPromedios")


# Panel lateral para mostrar el promedio
st.sidebar.title("Sistema de Gestión de Promedios")
promedio_final = 0  # Inicializar en cero


# Crear dos columnas
col1, col2 = st.columns(2)

with col1:
    # Sección del Examen
    with st.expander("Examen Final"):
        examen = st.number_input("Puntaje obtenido", min_value=0.0, max_value=12.0, value=0.0, step=1.0)

    # Complementos Extra
    with st.expander("Complementos Extra"):
        complemento_extra = 0
        if st.checkbox("Portada de la materia", value=False):
            complemento_extra = 2  # Valor de 2 puntos para el complemento extra

        # Agregar campos para puntos extra en examen y tareas
        complemento_extra_examen = st.number_input("Puntos Extra para Examen", min_value=0.0, max_value=4.0, value=0.0, step=1.0)
        complemento_extra_tareas = st.number_input("Puntos Extra para tareas", min_value=0.0, max_value=4.0, value=0.0, step=1.0)

    # Sección de Tareas
    with st.expander("Tareas"):
        # Selección del número de tareas utilizando un selectbox
        #cantidad_tareas = st.selectbox("Selecciona la cantidad de tareas", [1, 2, 3, 4, 5], index=0)
        cantidad_tareas = st.number_input("Selecciona la cantidad de tareas", min_value=1, max_value=5, value=1, step=1)

        # Lista para almacenar los puntos por tarea
        tareas = []

        # Calcular el valor de cada tarea en función de la cantidad seleccionada
        valor_por_tarea = 20 / cantidad_tareas  # Dividir 20 puntos entre la cantidad de tareas

        # Selección de tareas
        for i in range(cantidad_tareas):
            tarea = st.selectbox(f"Tarea {i+1}", ["No entregada", "Completa", "Justificada"], key=f"tarea_{i+1}")
            if tarea == "Completa":
                tareas.append(valor_por_tarea)  # Asignar valor proporcional a la tarea
            elif tarea == "Justificada":
                tareas.append(valor_por_tarea / 2)  # Tarea justificada tiene la mitad del valor
            elif tarea == "No entregada":
                tareas.append(0)  # No entregada tiene 0 puntos

with col2:

    # Sección de Actividades en Clase
    with st.expander("Actividades en Clase"):
        actividades = []
        for i in range(5):
            actividad = st.checkbox(f"Semana {i+1}", key=f"actividad_{i+1}")
            if actividad:
                actividades.append(4)  # Cada actividad suma 4 puntos
            else:
                actividades.append(0)  # Si no se marca, es inasistencia

    # Sección de Complementos Cualitativos
    with st.expander("Complementos Cualitativos"):
        complementos = []
        for i in range(5):
            complemento = st.checkbox(f"Complemento {i+1}", key=f"complemento_{i+1}")
            if complemento:
                puntaje = st.selectbox(f"Puntaje para Complemento {i+1}", ["Completo", "Retardo"], key=f"puntaje_{i+1}")
                if puntaje == "Completo":
                    complementos.append(4)  # Completo con 4 puntos
                elif puntaje == "Retardo":
                    complementos.append(2)  # Retardo con 2 puntos

    # Checkbox
    with st.expander("Mostrar QR"):
        mostrar_imagen = st.checkbox("Escanear QR para detalles de calificación")

if mostrar_imagen:
    st.image("qr.jpg", width=1000)



# Calcular el promedio final
promedio_final, examen_final, tareas_total, actividades_total, complementos_total = calcular_promedio(examen, tareas, actividades, complementos, complemento_extra_examen, complemento_extra_tareas, complemento_extra)

# Mostrar el promedio final en el panel lateral con el color adecuado
st.sidebar.subheader("Promedio Final:")
color = determinar_color(promedio_final)

# Contenedor sin color para el promedio final con un tamaño grande

st.sidebar.markdown(
    f"""
    <div style="padding: 10px; border-radius: 8px;">
        <h1 style="font-size: 120px; color:{color}; text-align:center;">{promedio_final:.2f}</h1>
    </div>
    """, unsafe_allow_html=True
)


# Rango de colores para el promedio
if color == 'red':
    st.sidebar.markdown("**Promedio en rango bajo (0-55)**")
elif color == 'darkorange':
    st.sidebar.markdown("**Promedio en rango medio (56-59)**")
elif color == 'green':
    st.sidebar.markdown("**Promedio en rango alto (60-100)**")
else:
    st.sidebar.markdown("**Promedio excelente (101-110)**")


# Campo para ingresar el ID del estudiante
st.sidebar.write("---")
id_estudiante = st.sidebar.text_input("ID del Estudiante", "")

# Opción para generar reporte detallado en el panel lateral
if st.sidebar.button("Generar Reporte General"):
    if id_estudiante:  # Verificar que el ID no esté vacío
        st.sidebar.write("---")
        st.sidebar.write("### Reporte General del Promedio Final")
        st.sidebar.write(f"**ID del Estudiante**: {id_estudiante}")
        st.sidebar.write(f"**Examen Final**: {examen_final:.2f} puntos")
        st.sidebar.write(f"**Tareas**: {tareas_total:.2f} puntos")
        st.sidebar.write(f"**Actividades en Clase**: {actividades_total:.2f} puntos")
        st.sidebar.write(f"**Complementos Cualitativos**: {complementos_total:.2f} puntos")
        st.sidebar.write(f"**Portada de la materia**: {complemento_extra:.2f} puntos")
        st.sidebar.write(f"**Puntaje Extra de Examen**: {complemento_extra_examen:.2f} puntos")
        st.sidebar.write(f"**Puntaje Extra de Tareas**: {complemento_extra_tareas:.2f} puntos")
        #st.sidebar.write(f"**Promedio Final Total**: {promedio_final:.2f} puntos")

        # Generar PDF con el ID del estudiante en el nombre del archivo
        pdf_file = generar_pdf(examen_final, tareas_total, actividades_total, complementos_total, complemento_extra, complemento_extra_examen, complemento_extra_tareas, promedio_final, actividades, id_estudiante)

        # Permitir que el usuario descargue el reporte detallado
        with open(pdf_file, "rb") as file:
            st.sidebar.download_button("Descargar Reporte General", file, file_name=f"reporte_general_{id_estudiante}.pdf", mime="application/pdf")
    else:
        st.sidebar.warning("Por favor ingresa el ID del estudiante antes de generar el reporte.")
