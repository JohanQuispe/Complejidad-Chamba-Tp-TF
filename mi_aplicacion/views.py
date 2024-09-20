from django.shortcuts import render, redirect
from .utils import generar_mapa
from .forms import CargarArchivoForm  # Solo importamos el formulario necesario
from .services import procesar_archivo  # Servicio que maneja la carga del archivo
from django.http import HttpResponse

# Vista principal
def home(request):
    return render(request, 'home.html')

# Vista para visualizar la red de internet
def visualizar_red(request):
    # Generamos el mapa con la función de utilidades
    mapa_html = generar_mapa()
    # Renderizamos la plantilla y pasamos el HTML del mapa
    return render(request, 'visualizar_red.html', {'mapa': mapa_html})

# Vista para optimizar rutas (aún sin funcionalidad)
def optimizar_rutas(request):
    return render(request, 'optimizar_rutas.html')

# Vista para cargar el archivo de nodos
def cargar_nodos(request):
    if request.method == 'POST':
        form = CargarArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            procesar_archivo(archivo)  # Llamamos a la función que procesa el archivo
            return redirect('home')
    else:
        form = CargarArchivoForm()

    return render(request, 'cargar_nodos.html', {'form': form})
