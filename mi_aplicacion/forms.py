from django import forms

class CargarArchivoForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo CSV')
