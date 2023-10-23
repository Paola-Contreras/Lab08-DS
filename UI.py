import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

animal_mapping = {'not acept': 0, 'acept': 1}
furniture_mapping = {'not furnished': 0, 'furnished': 1}
precio_predicho = 0


modelo = load_model('modelo_entrenado.h5')

def actualizar_etiqueta_precio(precio_predicho):
    precio_predicho = precio_predicho[0]
    output_label.config(text=f"Precio de alquiler estimado: ${precio_predicho:.2f}")


def predecir_precio(city, area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, rent_amount, property_tax, fire_insurance):
    # Codificar
    animal = animal_mapping.get(animal, 0)
    furniture = furniture_mapping.get(furniture, 0)
    data = [[area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, rent_amount, property_tax, fire_insurance]]

    # Predicción con el modelo
    precio_predicho = modelo.predict(data)[0]
    print(precio_predicho)
    actualizar_etiqueta_precio(precio_predicho)

    return precio_predicho

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Predicción de mercado inmobiliario en ciudades Brasileñas")
ventana.state('zoomed')

# h1
titulo_h1 = font.Font(family="Helvetica", size=28, weight="bold")
titulo_label = tk.Label(ventana, text="Predicción de mercado inmobiliario en ciudades Brasileñas", font=titulo_h1)
titulo_label.pack(side="top", fill="both", expand=True)

# Subtítulo
subtitulo_label = tk.Label(ventana, text="Ingresa los detalles de la propiedad:", font=font.Font(weight="bold"))
subtitulo_label.pack(pady=(5, 0))  # Reducir el espaciado en la parte superior

# Frame input
input_frame = tk.Frame(ventana)
input_frame.pack()

atributos = [
    "City", "Area", "Rooms", "Bathroom", "Parking Spaces", "Floor",
    "Animal", "Furniture", "HOA (R$)", "Rent Amount (R$)", "Property Tax (R$)", "Fire Insurance (R$)"
]

entry_widgets = {}

for atributo in atributos:
    label = tk.Label(input_frame, text=atributo, anchor="e", padx=1)
    label.grid(row=atributos.index(atributo), column=0, sticky='w')

    entry = tk.Entry(input_frame)
    entry.grid(row=atributos.index(atributo), column=1, columnspan=3, sticky='ew')
    entry_widgets[atributo] = entry

# Botón predicción
boton_prediccion = tk.Button(ventana, text="Realizar Predicción", command=lambda: predecir_precio(
    str(entry_widgets["City"].get() or 0),  
    int(entry_widgets["Area"].get() or 0),
    int(entry_widgets["Rooms"].get() or 0),
    int(entry_widgets["Bathroom"].get() or 0),
    int(entry_widgets["Parking Spaces"].get() or 0),
    int(entry_widgets["Floor"].get() or 0),
    str(entry_widgets["Animal"].get() or 0),
    str(entry_widgets["Furniture"].get() or 0),
    float(entry_widgets["HOA (R$)"].get() or 0.0),
    float(entry_widgets["Rent Amount (R$)"].get() or 0.0),
    float(entry_widgets["Property Tax (R$)"].get() or 0.0),
    float(entry_widgets["Fire Insurance (R$)"].get() or 0.0)
))
boton_prediccion.pack()

# Etiqueta para mostrar la predicción
output_label = tk.Label(ventana, text="", font=("Helvetica", 16))
output_label.pack()

# Subtítulo
subtitulo_label2 = tk.Label(ventana, text="Tendencias en Brazil", font=font.Font(weight="bold"))
subtitulo_label2.pack(pady=(5, 0))

# Info
info = tk.Label(ventana, text="En los siguientes gráficos se muestra información en donde se indican las tendencias de coste de vivienda en distintas ciudades de Brazil.", font=font.Font(weight="normal"))
info.pack(pady=(5, 0))

# Crear un Frame para las imágenes
image_frame = tk.Frame(ventana)
image_frame.pack(side="top", fill="both", expand=True)

# Cargar y escalar las imágenes
imagen1 = Image.open("./graficos/aceptAnimales.png")
imagen1 = imagen1.resize((400, 325))

imagen2 = Image.open("./graficos/promedio_por_ciudad.png")
imagen2 = imagen2.resize((400, 325))

imagen3 = Image.open("./graficos/roomsInfo.png")
imagen3 = imagen3.resize((400, 325))

imagen1_tk = ImageTk.PhotoImage(imagen1)
imagen2_tk = ImageTk.PhotoImage(imagen2)
imagen3_tk = ImageTk.PhotoImage(imagen3)

# Crear un Frame para las imágenes en una fila
image_row_frame = tk.Frame(image_frame)
image_row_frame.grid(row=0, column=0)

# Mostrar imágenes en el Frame en tres columnas
imagen1_label = tk.Label(image_row_frame, image=imagen1_tk)
imagen1_label.grid(row=0, column=0)

imagen2_label = tk.Label(image_row_frame, image=imagen2_tk)
imagen2_label.grid(row=0, column=1)

imagen3_label = tk.Label(image_row_frame, image=imagen3_tk)
imagen3_label.grid(row=0, column=2)

ventana.imagen1_tk = imagen1_tk
ventana.imagen2_tk = imagen2_tk
ventana.imagen3_tk = imagen3_tk

# Ejecutar la aplicación
ventana.mainloop()