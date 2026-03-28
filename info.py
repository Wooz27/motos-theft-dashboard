import pandas as pd
import json

class DatosRobos:
    #iniciar el objeto con la ruta del archivo y el data frame
    def __init__(self):
        self.ruta = ("data/data.json")
        self.datos = pd.read_json(self.ruta)
        self.df = pd.DataFrame(self.datos)
        self.datos["fecha_robo"] = pd.to_datetime(self.datos["fecha_robo"])
        
    def obtener_total_robos(self):
        return self.datos["id"].count()
    
    def obtener_dinero_perdido(self):
        return self.datos["valor_mxn"].sum()
    
    def obtener_marca_mas_robada(self):
        return self.datos["marca"].value_counts().idxmax()
    
    def obtener_modelo_mas_robado(self):
        return self.datos["modelo"].value_counts().idxmax()
    
    def obtener_mes_mas_robado(self):
        meses = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }
        
        return meses[self.datos["fecha_robo"].dt.month_name().value_counts().idxmax()]
    
    def promedio_valor_robos(self):
        return self.datos["valor_mxn"].mean()
    
    def obtener_horas_perdidas(self):
        prom= self.promedio_valor_robos()
        hora_pago = 34.75
        
        horas_perdidas = prom / hora_pago
        return horas_perdidas
    
    def obtener_horas_por_moto(self):
        self.datos["horas_perdidas"] = self.datos["valor_mxn"] / 34.75
        return self.datos[["id", "horas_perdidas"]]
    
        
    
    

if __name__ == "__main__":
    mi_reporte = DatosRobos()
    
    
    
    #para quien la mi codigo, esta seccion es para ver los resultados en consola. ingresa python info.py

    print(mi_reporte.obtener_total_robos())
    print(mi_reporte.obtener_dinero_perdido())
    print(mi_reporte.obtener_marca_mas_robada())
    print(mi_reporte.obtener_modelo_mas_robado())
    print(mi_reporte.obtener_mes_mas_robado())
    print(mi_reporte.promedio_valor_robos())
    print(mi_reporte.obtener_horas_perdidas())