import csv

# Asume que tienes modelos Nodo y Conexion definidos
from .models import Nodo, Conexion

def procesar_archivo(archivo):
    # Abrir el archivo en modo texto
    archivo = archivo.read().decode('utf-8').splitlines()
    reader = csv.reader(archivo)
    
    # Variable para diferenciar la sección del archivo que se está leyendo
    leyendo_nodos = True

    for fila in reader:
        if not fila or fila[0].startswith('#'):
            continue  # Saltar líneas vacías y comentarios
        
        if fila[0] == 'id':  # Fila de encabezado de nodos
            continue  # Saltar encabezados de nodos
        
        if fila[0] == 'origen':  # Inicia la sección de conexiones
            leyendo_nodos = False
            continue  # Saltar encabezado de conexiones

        if leyendo_nodos:
            # Procesar los nodos
            id_nodo, nombre, latitud, longitud = fila
            try:
                nodo = Nodo(id=id_nodo, nombre=nombre, latitud=float(latitud), longitud=float(longitud))
                nodo.save()
            except ValueError as e:
                print(f"Error al convertir los datos del nodo: {e}")
        else:
            # Procesar las conexiones (ahora incluyendo el peso)
            if len(fila) == 3:
                origen, destino, peso = fila
            else:
                origen, destino = fila
                peso = 1.0  # Asignar un peso por defecto si no se incluye

            try:
                nodo_origen = Nodo.objects.get(id=origen)
                nodo_destino = Nodo.objects.get(id=destino)
                conexion = Conexion(origen=nodo_origen, destino=nodo_destino, peso=float(peso))  # Añadir el peso
                conexion.save()
            except Nodo.DoesNotExist:
                print(f"Uno de los nodos especificados no existe: {origen} -> {destino}")
            except ValueError as e:
                print(f"Error al procesar el peso de la conexión: {e}")
