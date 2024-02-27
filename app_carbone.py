import streamlit as st
import pandas as pd
import plotly.express as px

from pandasai import SmartDataframe
from pandasai.llm import OpenAI

llm = OpenAI(api_token=st.secrets['OPENAI'])





st.set_page_config(layout='wide')


st.title(":panda_face: PanDa & Carbone :hammer:")
st.write("**Panama Data Consulting**")
st.markdown("##")

tab1, tab2, tab3 = st.tabs(["PanDa", "Nuestro Trabajo", "Propuesta"])

with tab2:

    st.subheader("1. Chatbots Brillantes")
    st.write("Asistentes virtuales potenciados por *ChatGPT*")
    st.write(" - Entrenados con información pública y privada")
    st.write(" - Disponibles 24/7")
    st.write(" - Capaces de captar datos y generar reportes")
    
    
    cl1, cl2, cl3 = st.columns([3,3,3])
    cl2.video("Chatbot Carbone.mp4", 'rb')
    
    st.markdown("##")
    
    st.subheader("2. Análisis de Datos para Todos")
    st.write("Tableros de inteligencia de negocios personalizados.")
    
    
    # Función para cargar y preparar los datos
    def cargar_datos():
        # Carga los datos desde el archivo CSV
        df = pd.read_csv('ventas_carbone.csv')
    
        # Convierte la columna 'Fecha' a tipo datetime y extrae el mes
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Mes'] = df['Fecha'].dt.month
        return df
    
    df = cargar_datos()
    
    # Sidebar con MultiSelect para los productos
    productos_seleccionados = st.multiselect(
        "Selecciona los productos",
        options=df['Producto'].unique(),
        default=df['Producto'].unique()
    )
    
    # Si no se selecciona ningún producto, se muestran todos
    if not productos_seleccionados:
        productos_seleccionados = df['Producto'].unique()
    
    # Filtrar datos basado en la selección
    df_filtrado = df[df['Producto'].isin(productos_seleccionados)]
    
    # Line Chart - Ventas por mes en términos de valor monetario
    col1, col2 = st.columns(2)
    ventas_por_mes = df_filtrado.groupby(['Mes', 'Producto'])['Subtotal'].sum().reset_index(name='Ventas ($)')
    fig_line = px.line(ventas_por_mes, x='Mes', y='Ventas ($)', color='Producto', title='Ventas por Mes ($)')
    fig_line.update_layout(legend=dict(orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))
    col1.plotly_chart(fig_line)
    
    # Bar Chart - Ventas Totales por Producto en términos de valor monetario
    ventas_totales = df_filtrado.groupby('Producto')['Subtotal'].sum().reset_index(name='Ventas Totales ($)')
    fig_bar = px.bar(ventas_totales, x='Producto', y='Ventas Totales ($)', color='Producto', title='Ventas Totales por Producto ($)')
    fig_bar.update_layout(legend=dict(orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))
    col2.plotly_chart(fig_bar)
    
    # Pie Chart - Unidades Vendidas por Producto (sin leyenda)
    unidades_vendidas = df_filtrado.groupby('Producto')['Unidades'].sum().reset_index(name='Unidades Vendidas')
    fig_pie = px.pie(unidades_vendidas, names='Producto', values='Unidades Vendidas', title='Unidades Vendidas por Producto')
    fig_pie.update_layout(showlegend=False)
    col1.plotly_chart(fig_pie)
    
    # Pivot Table - Ventas totales, unidades vendidas y porcentaje del total
    total_ventas = ventas_totales['Ventas Totales ($)'].sum()
    unidades_por_producto = df_filtrado.groupby('Producto')['Unidades'].sum().reset_index(name='Unidades Vendidas')
    ventas_y_unidades = pd.merge(ventas_totales, unidades_por_producto, on='Producto')
    ventas_y_unidades['Porcentaje del Total (%)'] = ((ventas_y_unidades['Ventas Totales ($)'] / total_ventas) * 100).round(2)
    ventas_y_unidades['Porcentaje del Total (%)'] = ventas_y_unidades['Porcentaje del Total (%)'].astype(str) + '%'
    
    col2.write("**Tabla Resumen**")
    col2.dataframe(ventas_y_unidades, hide_index=True)
    
    
    
    # Preguntas
    
    
    prompt = st.text_area("**Pregúntale algo a la data :magic_wand:**")
    adf = SmartDataframe(df, config={'llm':llm})
    
    st.info('Puedes hacer preguntas como: "Cual fue el producto mas vendido y cuantas unidades se vendieron?", "Que porcentaje de clientes compró martillos?", "Cuanto suma la venta de destornilladores y taladros?"')
    # Generate output
    if st.button("Preguntar"):
        if prompt:
            # call pandas_ai.run(), passing dataframe and prompt
            with st.spinner("Pensando..."):
                respuesta = adf.chat(f"{prompt}. si tu respuesta es un porcentaje, asegurate de que el formato de tu respuesta incluya dos decimales y el símbolo %. Si tu respuesta es una cifra monetaria, debe tener dos decimales y el símbolo $ al principio. Si la pregunta es irrelevante, responde 'intenta otra pregunta'. Tus respuestas deben ser oraciones completas en español y debes explicar como llegaste al resultado.")
                st.write(respuesta)
        else:
            pass
    
    
    
    
    
    
    
    
    st.markdown("####")
    
    st.subheader("3. Automatización de Procesos y Aplicaciones Integrales")
    st.write("Utilizando las herramientas más versátiles y avanzadas del mercado, desarrollamos soluciones a la medida a una velocidad incomparable.")
    st.markdown("###")
    col1, col2, col3 = st.columns(3)
    
    col1.image("python logo.jpeg")
    col2.image("bubble logo.jpeg")
    col3.image("chatgpt logo.png")
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1.expander("Python"):
        st.write("Python es el lenguaje número 1 entre desarroladores de software. En PanDa :panda_face:, Python es la base de todas nuestras soluciones.")
    
    
    with col2.expander("Bubble.io"):
        st.write("Existen infinitas alternativas para desarrollar aplicaciones, pero ninguna como Bubble. Por su velocidad y versatilidad, Bubble es nuestra herramienta de elección para el desarrollo de *business apps* personalizadas.")
    
    
    with col3.expander("ChatGPT"):
        st.write("ChatGPT abrió el universo de la inteligencia artificial para todo el que quiera aprovecharlo, nosotros ya nos montamos en la ola. :surfer:")

with tab1:

    st.subheader("Qué es PanDa")

    st.markdown('''En PanDa, entendemos que cada empresa es única, con desafíos y necesidades distintas. Nuestro enfoque no es vender soluciones prefabricadas en un proceso estático de descubrimiento, experimentación y desarrollo. Al contrario, observamos que este método tradicional a menudo conduce a conclusiones predecibles, que no solo son ineficaces sino que también interfieren con el rendimiento de los empleados y requieren de inversiones significativas en herramientas costosas.

Nuestra filosofía se centra en la personalización y la eficiencia. Comenzamos desde la perspectiva de los empleados, abordando cada pequeña ineficiencia con herramientas diseñadas a medida para mejorar su efectividad y eficiencia. Nuestro objetivo es siempre buscar el camino de menor resistencia, creando soluciones que se integren armoniosamente con las operaciones existentes de nuestros clientes.

Por ejemplo, en lugar de reconstruir bases de datos completas o implementar sistemas ERP de vanguardia, utilizamos tecnologías accesibles como Python y Streamlit para desarrollar herramientas personalizadas que permiten visualizar datos desde archivos CSV. Esta estrategia nos ha permitido construir dashboards descriptivos, modelos de pronóstico, segmentaciones de clientes y herramientas de recomendación de productos que empoderan a los vendedores en las calles para aumentar sus ventas por cliente.

Además, hemos adoptado enfoques innovadores como el uso de Bubble.io para el desarrollo rápido de aplicaciones tácticas que se integran con APIs de terceros, aprovechando las ventajas de las plataformas no-code y low-code para reducir significativamente nuestros tiempos de desarrollo.

Un caso de éxito notable fue el desarrollo de un extractor de datos de PDFs para un cliente, automatizando el proceso de generación de órdenes de compra en su sistema ERP, una tarea que previamente se realizaba manualmente. Este tipo de soluciones demuestra nuestra capacidad para transformar procesos complejos en operaciones eficientes y automatizadas.

Nuestra consultoría abarca tres categorías principales: automatización de procesos, análisis de datos e implementación de inteligencia artificial. Mientras que las dos primeras categorías representan nuestra base, es en el campo de la inteligencia artificial donde encontramos el potencial más emocionante y revolucionario. Más allá de las aplicaciones obvias en ventas y atención al cliente, estamos explorando cómo la IA puede transformar otras áreas, como la creación de herramientas para grabar y resumir el contenido de reuniones, o desarrollar repositorios de información personalizada para clientes.

En PanDa, no solo estamos comprometidos con el desarrollo de soluciones tecnológicas avanzadas; estamos redefiniendo lo que significa ser una consultoría de tecnología en el siglo XXI. Con un enfoque en soluciones personalizadas, eficiencia y la vanguardia de la innovación, PanDa está preparada para liderar a las empresas hacia un futuro digital más inteligente y adaptado a sus necesidades únicas.''')

with tab3:
    st.subheader("Propuesta Comercial"):
    st.markdown('''Nuestro modelo de negocio en Panama Data Consulting (PanDa) se basa en una relación de colaboración continua con nuestros clientes. Ofrecemos un servicio de suscripción mensual a un costo fijo de $2400, que permite a nuestros clientes acceder a nuestro equipo de desarrollo para trabajar en soluciones personalizadas, una a la vez. Este enfoque garantiza que cada proyecto reciba la atención detallada que merece, maximizando el valor y la efectividad de cada solución.

La suscripción mensual incluye:

Desarrollo de herramientas a medida basado en las necesidades específicas del cliente.
Trabajo en proyectos de manera secuencial, asegurando calidad y enfoque.
Sin costos ocultos para el acceso a las herramientas desarrolladas.
Los costos asociados con servicios de terceros, como APIs o herramientas específicas pagadas, no están incluidos en la tarifa mensual. Sin embargo, la decisión de utilizar estas herramientas de terceros se basa siempre en un análisis cuidadoso del retorno de la inversión (ROI), con el objetivo de asegurar que el uso de cualquier servicio adicional justifique su costo.

Nuestra meta es ser más que un proveedor; queremos ser parte del equipo de nuestros clientes, construyendo sobre la infraestructura existente y adaptándonos a sus necesidades cambiantes con soluciones eficientes y efectivas. Este modelo no solo ofrece claridad y previsibilidad en los costos, sino que también fomenta una asociación estratégica a largo plazo, centrada en el crecimiento y la innovación continua.''')


