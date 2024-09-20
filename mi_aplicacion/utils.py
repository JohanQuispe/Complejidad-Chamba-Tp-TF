import folium
import requests
import polyline  # Importamos la librería polyline para decodificar la ruta
from .models import Nodo, Conexion  # Importamos los modelos


def obtener_ruta_osrm(origen, destino):
    # URL de la API de OSRM para obtener rutas de manejo entre dos puntos
    url = f"http://router.project-osrm.org/route/v1/driving/{origen[1]},{origen[0]};{destino[1]},{destino[0]}?overview=full"
    response = requests.get(url)
    data = response.json()

    if data['routes']:
        # Extraemos la ruta codificada de la respuesta
        ruta_codificada = data['routes'][0]['geometry']
        # Decodificamos la geometría de la ruta usando polyline
        puntos_ruta = polyline.decode(ruta_codificada)
        # Retornamos la ruta como una lista de puntos
        return puntos_ruta
    return None


def generar_mapa():
    # Crear un mapa centrado en Lima, Perú
    mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=13)

    # Añadir nodos al mapa
    nodos = Nodo.objects.all()
    for nodo in nodos:
        folium.Marker([nodo.latitud, nodo.longitud], popup=nodo.nombre).add_to(mapa)

    # Añadir conexiones entre los nodos utilizando rutas de OSRM
    conexiones = Conexion.objects.all()
    for conexion in conexiones:
        origen = [conexion.origen.latitud, conexion.origen.longitud]
        destino = [conexion.destino.latitud, conexion.destino.longitud]

        # Obtener la ruta real usando OSRM
        puntos_ruta = obtener_ruta_osrm(origen, destino)
        
        if puntos_ruta:
            # Dibujar la ruta obtenida desde OSRM
            folium.PolyLine(locations=puntos_ruta, color="blue").add_to(mapa)
        else:
            # Si no se pudo obtener la ruta, dibujar línea directa
            folium.PolyLine(locations=[origen, destino], color="red").add_to(mapa)

    # Convertir el mapa a HTML
    return mapa._repr_html_()
