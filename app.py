import pandas as pd
import dash 
from dash import dcc,html,Input,Output
import plotly.express as px

#cargar los datos excel
Dataf = pd.read_excel('notas_estudiantes_limpio.xlsx')
print(Dataf)

#inicializar la app
Estanotas = dash.Dash(__name__)
Estanotas.title = 'Estadistica notas'
#crear el layout
Estanotas.layout = html.Div([
    #crear el titulo del tablero
    html.H1("Tablero de notas de estudiantes", style={"textAlign":"center",
        "color":"#6912ec",
        "padding":"20px",
        "fontFamily":"Arrial",
        "backgroundColor":"#E9ECEE"
    }),
#crear la barra de seleccion de materias
     html.Label("Seleccionar una materia: ",style={"margin":"10px"}),
     dcc.Dropdown(id="filtro_materia",
                 options=[{"label": carrera, "value": carrera} for carrera in sorted(Dataf["Carrera"].unique())],
                 value=Dataf["Carrera"].unique()[0],
                 style={"width":"100%","margin":"auto"}
                 ),
     html.Br(),
 #crear los tabs 
     dcc.Tabs([
         dcc.Tab(label='Grafico de promedios',children=[dcc.Graph(id='histograma')

           ]),
         dcc.Tab(label="Edad vs Promedio",children=[dcc.Graph(id='dispersion')
          ]), 
           dcc.Tab(label="Desempeño",children=[dcc.Graph(id='pie')
          ]),
           dcc.Tab(label="Promedio notas x carrera ",children=[dcc.Graph(id='barras')
          ]),
     ], style={"fontWeight":"bold","color":"#2c3e50"})  
])  

#actualizar el grafico
@Estanotas.callback(
        #se llama los outputs creados en el layout
          Output("histograma", "figure"),
          Output("dispersion", "figure"),
          Output ("pie", "figure"),
          Output ("barras", "figure"),
          Input("filtro_materia", 'value')

)
#funcion para actualizar el grafico
def actualizar(filtro_materia):
    filtro= Dataf[Dataf["Carrera"]==filtro_materia] 

    #crear los grafficos
    # grafico tipo histograma
    histo = px.histogram(filtro, x="Promedio",nbins=10,title=f"Distribuccion de promedios - {filtro_materia}",
                         color_discrete_sequence=["#3498db"]).update_layout(template="plotly_dark",yaxis_title="Cantidad de estudiantes")
    #grafico de dispersion
    disper = px.scatter(filtro,x="Edad",y="Promedio",color="Desempeño",title=f"Edad vs Promedio - {filtro_materia}",
                        color_discrete_sequence=px.colors.qualitative.Set2).update_layout(template="plotly_dark")  

    #Pie
    pi = px.pie(filtro, names="Desempeño", values="Promedio", title=f"Desempeño - {filtro_materia}", 
                color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(template="plotly_dark")
    
    #Barras: groupby para agrupar al iniciar dashboard
    promedios = filtro.groupby("Carrera")["Promedio"].mean().reset_index()
    barr=px.bar(promedios, x="Carrera",y="Promedio", title="Promedio de notas por carrera",
                color="Carrera", color_discrete_sequence=px.colors.qualitative.Prism).update_layout(template="plotly_dark")
    return histo,disper, pi, barr

#Ejecutar la aplicacion
if __name__ == '__main__':
    Estanotas.run(debug=True)
    
    #plotly_plotly+
    #pip install gunicorn
    #pip freeze > requirements.txt, requerimientos sistema
    #Toca nombre app + archivo procfile
    #quitar credencial windows github paa eviar conflictos


 