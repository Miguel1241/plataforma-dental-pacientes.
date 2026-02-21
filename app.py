import streamlit as st
import psycopg2

def conectar_db():
    return psycopg2.connect(
        host="127.0.0.1",
        database="Consultorio_db",
        user="postgres",
        password="tesis123",
        port="5432"
    )

st.title("🦷 Portal del Paciente - Clínica Dental")

id_buscar = st.text_input("Ingresa tu ID de Paciente:")

if st.button("Consultar Historial"):
    conn = conectar_db()
    cur = conn.cursor()
    query = """
    SELECT p.nombre, p.apellido, h.alergias, h.padecimientos, h.fecha_registro
    FROM pacientes p
    JOIN historial_clinico h ON p.id_paciente = h.id_paciente
    WHERE p.id_paciente = %s
    """
    cur.execute(query, (id_buscar,))
    resultado = cur.fetchone()
    
    if resultado:
        st.success(f"Bienvenido, {resultado[0]} {resultado[1]}")
        st.write(f"*Alergias:* {resultado[2]}")
        st.write(f"*Padecimientos:* {resultado[3]}")
        st.write(f"*Fecha de registro:* {resultado[4]}")
    else:
        st.error("Paciente no encontrado.")
    
    cur.close()
    conn.close()
