import streamlit as st
import psycopg2

def conectar_db():
    try:
        # Usamos tu nuevo túnel y aumentamos el timeout para evitar errores
        conn = psycopg2.connect(
            host="hboxukrfm3.loclx.io", 
            port=80,
            database="Consultorio_db",
            user="postgres",
            password="tesis123",
            connect_timeout=20
        )
        return conn
    except Exception as e:
        st.error(f"Error detectado: {e}")
        return None

st.sidebar.title("Menú Principal")
opcion = st.sidebar.selectbox("Selecciona una vista:", ["Portal Paciente", "Panel Dentista (Admin)"])

if opcion == "Portal Paciente":
    st.header("🦷 Portal del Paciente")
    id_buscar = st.text_input("Ingresa tu ID de Paciente:")
    
    if st.button("Consultar"):
        if id_buscar:
            conn = conectar_db()
            if conn:
                cur = conn.cursor()
                # Consulta corregida para traer los datos del historial
                cur.execute("SELECT * FROM historial_clinico WHERE id_paciente = %s", (id_buscar,))
                paciente = cur.fetchone()
                
                if paciente:
                    st.success(f"¡Paciente encontrado!")
                    st.write(f"*Alergias:* {paciente[1]}")
                    st.write(f"*Padecimientos:* {paciente[2]}")
                    st.write(f"*Observaciones:* {paciente[3]}")
                else:
                    st.warning("No se encontró ningún paciente con ese ID.")
                
                cur.close()
                conn.close()
        else:
            st.warning("Por favor, ingresa un ID válido.")

elif opcion == "Panel Dentista (Admin)":
    st.header("👨‍⚕️ Panel de Control Odontológico")
    
    with st.expander("Registrar Nuevo Historial Clínico"):
        id_paciente = st.number_input("ID del Paciente:", min_value=1)
        alergias = st.text_area("Alergias:")
        padecimientos = st.text_area("Padecimientos:")
        observaciones = st.text_area("Observaciones Médicas:")
        
        if st.button("Guardar Registro"):
            conn = conectar_db()
            if conn:
                try:
                    cur = conn.cursor()
                    query = """INSERT INTO historial_clinico (id_paciente, alergias, padecimientos, observaciones) 
                               VALUES (%s, %s, %s, %s)"""
                    cur.execute(query, (id_paciente, alergias, padecimientos, observaciones))
                    conn.commit()
                    st.success("¡Historial registrado con éxito!")
                    cur.close()
                    conn.close()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

    if st.button("Ver Todos los Pacientes"):
        conn = conectar_db()
        if conn:
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM historial_clinico", conn)
            st.dataframe(df)
            st.write("Lista completa de historiales clínicos registrados.")
            conn.close()
