import os
import base64
import pandas as pd
import streamlit as st
import altair as alt
from info import DatosRobos
from streamlit_extras.metric_cards import style_metric_cards


# ==========================================
# UTILIDADES Y CONVERSIONES
# ==========================================
def formato_moneda(valor):
    return f"${valor:,.2f}"

def ruta_a_base64(ruta): # Esta función resuelve problemas de Streamlit con imágenes locales pasándolas a base64 para evitar censura del navegador.
    if pd.isna(ruta) or not str(ruta).strip(): 
        return None
        
    ruta_limpia = str(ruta).replace("app/static/", "")
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta_limpia)
    
    if os.path.exists(ruta_completa):
        try:
            with open(ruta_completa, "rb") as image_file:
                ext = ruta_completa.split('.')[-1].lower()
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:image/{ext};base64,{encoded}"
        except Exception:
            return None
    return None


# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN E INSTANCIAS
# ==========================================
def main():
    st.set_page_config(
        page_title="Alerta Tizimín, la perdida del enfuerzo",
        page_icon="🚨",
        layout="centered",
    )

    info = DatosRobos()
    
    total_motos = info.obtener_total_robos()
    valor_total_perdido = info.obtener_dinero_perdido()
    marca_estrella = info.obtener_marca_mas_robada()
    modelo_estrella = info.obtener_modelo_mas_robado()
    peor_mes = info.obtener_mes_mas_robado()

    # ==========================================
    # SECCIÓN: INTRODUCCIÓN
    # ==========================================
    st.title("🚨 Epidemia sobre ruedas: La crisis de robos de motos en Tizimín")
    st.write("")
    st.markdown("""
    **¿Sabías cuántas motos nos han arrebatado de las manos en los primeros meses del año?**
    Lo que parecían ser casos aislados se ha convertido en una herida constante al patrimonio de las familias tizimileñas. 
    
    A través del rastreo de denuncias ciudadanas, este reporte transparenta las cifras, los montos perdidos y cuáles son los blancos favoritos de la delincuencia.
    Desliza para entender a qué nos enfrentamos 👇
    """)

    st.divider()
    
    st.info("Este reporte aún no está completo, solo es una muestra de lo que estoy trabajando y me ayudarían mucho si me pudieran brindar reportes para tomar en cuenta, ya que solo encontré 9.")

    # ==========================================
    # SECCIÓN 1: IMPACTO ECONÓMICO
    # ==========================================
    st.subheader("1. El golpe directo al bolsillo 💸")
    st.markdown(f"""
    No es solo "una moto más" desaparecida frente a la tienda, es una herramienta de trabajo, el transporte escolar y un esfuerzo económico tirado a la basura. 
    En los registros actuales, **las pérdidas económicas reportadas superan los {formato_moneda(valor_total_perdido)} MXN.** 
    """)
    
    col1, col2 = st.columns(2)
    col1.metric(label="Motos Robadas Reportadas", value=total_motos)
    col2.metric(label="Pérdidas Acumuladas", value=formato_moneda(valor_total_perdido))
    
    style_metric_cards(
        background_color="#1c1c1c", 
        border_color="#ffffff", 
        border_size_px=2, 
        border_radius_px=10 
    )

    st.caption("Fuente: Consolidación de denuncias públicas en redes sociales, 2026.")
    st.divider()

    # ==========================================
    # SECCIÓN 2: PATRONES DE ROBO
    # ==========================================
    st.subheader("2. Las favoritas de los rateros 🎯")
    st.markdown("""
    Los ladrones no están agarrando lo primero que ven, ya están seleccionando, analizando marcas y operando con un "menú" en la cabeza. ¿Qué están buscando?
    """)
    
    col3, col4, col5 = st.columns(3)
    col3.metric(label="Marca más robada", value=marca_estrella)
    col4.metric(label="Modelo más buscado", value=modelo_estrella)
    col5.metric(label="Mes más peligroso", value=peor_mes)

    st.warning(f"""
    👁️‍🗨️ **Ojo al dato:** Si transitas por la ciudad en una **{marca_estrella} (especialmente modelo {modelo_estrella})**, las estadísticas indican que estás manejando la moto más codiciada por el mercado negro local. 
    El método de "jalón de llaves" es el preferido: no dejes tu vehículo sin seguro ni un segundo.
    """)

    st.divider()
    # ==========================================
    # SECCIÓN 3: IMPACTO ECONÓMICO 
    # ==========================================
    
    st.subheader("3. Reportes y sus precios 📉")
    
    st.markdown("En los siguientes elementos se detalla cuanto tiempo debe invertir un trabajador con sueldo promedio para comprar su moto")
    
    
    df_robos_moto = pd.DataFrame({
        "motos": info.datos["id"].astype(str), 
        "valor": info.datos["valor_mxn"],
        "marca": info.datos["marca"],
        "horas": info.obtener_horas_por_moto()["horas_perdidas"]
    })
    
    grafica_valor = alt.Chart(df_robos_moto).mark_bar().encode(
        y= alt.Y("motos", sort='-x', axis=alt.Axis(title="ID de Moto", labelAngle=0)),
        x= alt.X("valor", axis=alt.Axis(title="Pérdida estimada (MXN)")),
        color= alt.Color("marca:N", title="Marca", scale=alt.Scale(scheme="category20")),
        tooltip=["motos", "marca", "valor"]
    )
    
    st.altair_chart(grafica_valor, width="stretch")
    
    grafica_horas = alt.Chart(df_robos_moto).mark_bar().encode(
        y= alt.Y("motos", sort='-x', axis=alt.Axis(title="ID de Moto", labelAngle=0)),
        x= alt.X("horas", axis=alt.Axis(title="Horas de trabajo perdidas")),
        color= alt.Color("marca:N", title="Marca", scale=alt.Scale(scheme="category20")),
        tooltip=["motos", "marca", "horas"]
    )
    
    st.altair_chart(grafica_horas, width="stretch")
    
    horas_perdidas = info.obtener_horas_perdidas()
    col1,col2,col3 = st.columns([1,1.3,1])
    col1.metric(label="Valor Promedio de Robo", value=formato_moneda(info.promedio_valor_robos()))
    col2.metric(label="Horas de trabajo necesarias para comprar", value=f"{horas_perdidas:.1f} horas")
    col3.metric(label="Valor por Hora Perdida", value=formato_moneda(34.75))
    
    style_metric_cards(
        background_color="#1c1c1c", 
        border_color="#ffffff", 
        border_size_px=2, 
        border_radius_px=10 
    )

    
    

    # ==========================================
    # SECCIÓN 4: TABLA DE DATOS
    # ==========================================
    st.divider()
    st.subheader("4. Registro Público de Robos")
    st.markdown("Consulta el detalle de los incidentes que tenemos registrados a continuación:")
    
    df_mostrar = info.datos.copy()
    df_mostrar["img"] = df_mostrar["img"].apply(ruta_a_base64)
    
    columnas_ordenadas = ['img'] + [col for col in df_mostrar.columns if col not in ['img', 'id']]
    df_mostrar = df_mostrar[columnas_ordenadas]
    
    st.dataframe(
        df_mostrar,
        column_config={
            "img": st.column_config.ImageColumn(
                "Foto",
                help="Imagen de la publicación original"
            ),
            "fuente_url": st.column_config.LinkColumn(
                "Enlace FB",
                display_text="Ver reporte"
            )
        },
        width="stretch",
        hide_index=True
    )
    
    # ==========================================
    # SECCIÓN 5: CONCLUSIÓN Y CONTEXTO
    # ==========================================
    st.divider()
    st.subheader("5. De la indignación a la prevención")
    st.markdown("""
    Cada reporte representa el patrimonio robado de un trabajador. Y hasta que no existan soluciones firmes, la prevención vecinal y el cuidado mutuo (como candados de disco) son la única línea de defensa.
    """)

    st.info("👋 **Sobre este reporte:** Este tablero es una iniciativa independiente creada por Reynaldo Manzanilla, estudiante de Data Science en IEU Puebla. El objetivo es dar visibilidad al daño económico y patrones que afectan la paz social en Tizimín, transformando los avisos de auxilio de Facebook en datos medibles.")

if __name__ == "__main__":
    main()
