import streamlit as st
import psycopg2
def conectar_db():
    try:
        conn = psycopg2.connect(
            host="dncz6ejujh.loclx.io", # Verifica que este siga verde en Ubuntu
            port=443, # Cambiamos a 443 para saltar bloqueos
            database="Consultorio_db",
            user="postgres",
            password="tesis123"
        )
        return conn
    except Exception as e:
        st.error(f"Error: {e}")
        return None
    
st.sidebar.title("Menú Principal")
opcion = st.sidebar.selectbox("Selecciona una vista:", ["Portal Paciente", "Panel Dentista (Admin)"])

if opcion == "Portal Paciente":
    st.header("🦷 Portal del Paciente")
    id_buscar = st.text_input("Ingresa tu ID de Paciente:")
    if st.button("Consultar"):
        pass

elif opcion == "Panel Dentista (Admin)":
    st.header("👨‍⚕️ Panel de Control Odontológico")
    
    with st.expander("Registrar Nuevo Historial Clínico"):
        id_paciente = st.number_input("ID del Paciente:", min_value=1)
        alergias = st.text_area("Alergias:")
        padecimientos = st.text_area("Padecimientos:")
        observaciones = st.text_area("Observaciones Médicas:")
        
        if st.button("Guardar Registro"):
            try:
                conn = conectar_db()
                cur = conn.cursor()
                query = """
                INSERT INTO historial_clinico (id_paciente, alergias, padecimientos, observaciones)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(query, (id_paciente, alergias, padecimientos, observaciones))
                conn.commit()
                st.success("¡Historial registrado con éxito!")
                cur.close()
                conn.close()
            except Exception as e:
                st.error(f"Error al guardar: {e}")

    if st.button("Ver Todos los Pacientes"):
        conn = conectar_db()
        df = st.dataframe(conn) 
        st.write("Lista completa de historiales clínicos registrados.")
