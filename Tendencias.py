import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
import matplotlib.pyplot as plt
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import argrelextrema
from PIL import Image, ImageTk, ImageFilter
from datetime import datetime, timedelta

serie_numeros = []
resultado_final = []
resultado_final_check =[]
historial_resultados = []
plt.style.use('ggplot')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')  # Establece el nivel de registro a "warning" o superior
global navegador 
global driver   
driver = webdriver.Chrome(options=chrome_options)
def iniciar_sesion_y_navegar(usuario, contrasena):
    try:
   
        driver.get('https://betplay.com.co/')
        
        iframe_id = 'gameFrame'
        iframe_secundario_id = 'spribe-game'
        
        # Encontrar los elementos de nombre de usuario, contraseña y botón de inicio de sesión
        username_elem = driver.find_element(By.ID, "userName")
        password_elem = driver.find_element(By.ID, "password")
        login_button_elem = driver.find_element(By.ID, "btnLoginPrimary")

        # Ingresar credenciales
        username_elem.send_keys(usuario)
        password_elem.send_keys(contrasena)
        
        # Hacer clic en el botón de inicio de sesión
        login_button_elem.click()
        
        # Esperar a que la página se cargue completamente
        wait = WebDriverWait(driver, 30)
        wait.until(EC.url_to_be("https://betplay.com.co/"))
        
        time.sleep(10)
        
        driver.get("https://betplay.com.co/slots/launchGame?gameCode=SPB_aviator&flashClient=true&additionalParam=&integrationChannelCode=PARIPLAY")
        
        # Resto del código...
                # Cambiar al iframe principal
        while len(driver.find_elements(By.ID, iframe_id)) == 0:
            time.sleep(2)
            print(' No encontrado..')

        iframe = driver.find_element(By.ID, iframe_id)
        iframe_id_value = iframe.get_attribute('id')
        driver.switch_to.frame(iframe_id_value)

        # Cambiar al iframe secundario
        while len(driver.find_elements(By.ID, iframe_secundario_id)) == 0:
            time.sleep(2)
            print('Conectando...')

        iframe2 = driver.find_element(By.ID, iframe_secundario_id)
        iframe_id_value2 = iframe2.get_attribute('id')
        driver.switch_to.frame(iframe_id_value2)

        # Verificar si el elemento deseado está presente
        while len(driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]')) == 0:
            time.sleep(2)
            print('No encontrado2')

        elemento = driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]')

        # Imprimir el texto del primer elemento de la lista (si hay elementos)
        if elemento:
            texto = elemento[0].text
        else:
            print("No se encontraron elementos")
        
        return driver  # Devolver el objeto del navegador
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return None
    finally:
        # No cerrar el navegador aquí; el llamante deberá hacerlo manualmente
        pass
def iniciar_sesion_desde_interfaz():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Agregar un icono a la ventana
       
      
    icono_path = os.path.join(directorio_actual, "lock.ico")  # Reemplaza con el nombre de tu icono
    ventana.iconbitmap(icono_path)
     # Establecer el tamaño de la ventana en píxeles (ancho x alto)
    ventana.geometry("500x300")

        # Crear un objeto de estilo
    estilo = ttk.Style()

        # Configurar el estilo del campo de entrada
    estilo.configure('TEntry', padding=(10, 5), font=('Arial', 12))


    # Variables para almacenar el usuario y la contraseña
    usuario_var = tk.StringVar()
    contrasena_var = tk.StringVar()

    # Función para manejar el clic en el botón de inicio de sesión
    def clic_en_iniciar_sesion():
        global navegador 
        usuario = usuario_var.get()
        contrasena = contrasena_var.get()

        # Llamar a la función de inicio de sesión
        navegador = iniciar_sesion_y_navegar(usuario, contrasena)

        # Cerrar la ventana después de iniciar sesión
        #ventana.destroy()

    # Crear etiquetas, campos de entrada y botón en la interfaz
    
   
    
    etiqueta_usuario = ttk.Label(ventana, text="Usuario:")
    entrada_usuario = ttk.Entry(ventana, textvariable=usuario_var)
    etiqueta_contrasena = ttk.Label(ventana, text="Contraseña:")
    entrada_contrasena = ttk.Entry(ventana, textvariable=contrasena_var, show="*")
    boton_iniciar_sesion = ttk.Button(ventana, text="Iniciar Sesión", command=clic_en_iniciar_sesion)

    # Posicionar elementos en la ventana
    etiqueta_usuario.pack(pady=10)
    entrada_usuario.pack(pady=10)
    etiqueta_contrasena.pack(pady=10)
    entrada_contrasena.pack(pady=10)
    boton_iniciar_sesion.pack(pady=10)

    # Iniciar el bucle de eventos de la interfaz
    ventana.mainloop()
def obtener_texto_elemento(elemento):
    try:
        # Intenta obtener el texto del elemento
        texto_elemento = elemento.text
        return texto_elemento
    except StaleElementReferenceException:
        # Si se produce una StaleElementReferenceException, intenta volver a localizar el elemento
        return None   
def resultado2():
    global resultado_final
    
    #elementos = driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]')
    # Esperar hasta que al menos un elemento esté presente
    elementos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]'))
    )
    
    #resultado_final = []
    
    for elemento in elementos:
        resultado=obtener_texto_elemento(elemento)
        

        if resultado != None:
            #texto_elemento = elemento.text
            texto_elemento=resultado
            numero = texto_elemento.split('x')[0].replace(',', '.')  # Tomar la parte antes de 'x' y reemplazar ',' por '.'
            #resultado_final.append(float(numero))
            resultado_final=numero
            #print(resultado_final)
        
    
    return resultado_final
def ejecutora():
    while True:
        resultado2()   
# Llamar a la función de inicio de sesión desde la interfaz

class InterfazGrafica:
    def __init__(self):
        self.serie_numeros = []
        self.num_mayores_a_2 = 0
        self.num_menores_a_2 = 0
        
        
        # Variable para el tiempo restante en el cronómetro
        self.tiempo_restante = timedelta(minutes=1, seconds=20)
        # Variable para almacenar el tiempo de inicio del cronómetro
        self.tiempo_inicio_cronometro = None
        # Variable para indicar si el cronómetro está activo
        self.cronometro_activo = False
       
        # Inicializar el atributo driver
        self.driver = None
        self.ventana = tk.Tk()
        self.ventana.title("Analizador de Tendencias  Aviator  >-|->")
        label_texto = tk.Label(self.ventana, text="Creador: Eduardo Fuentes ")
        correo = tk.Label(self.ventana, text="egfuentesc@gmail.com ")
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Agregar un icono a la ventana
        # Agregar un Label para el reloj digital
        self.reloj_label = tk.Label(self.ventana, font=('calibri', 40, 'bold'), background='black', foreground='white')
        self.reloj_label.pack(anchor='center', pady=20)
        
         # Agregar imágenes
        icono_arriba = os.path.join(directorio_actual, "arriba.png")
        icono_abajo = os.path.join(directorio_actual, "abajo.png")
    
        img_mayores_a_2 = tk.PhotoImage(file=(icono_arriba) ).subsample(4, 4) # Reemplazar con la ruta de tu imagen
        img_menores_a_2 = tk.PhotoImage(file=(icono_abajo) ).subsample(4, 4) # Reemplazar con la ruta de tu imagen
        # Crear Labels para las imágenes
        label_img_mayores_a_2 = tk.Label(self.ventana, image=img_mayores_a_2)
        label_img_menores_a_2 = tk.Label(self.ventana, image=img_menores_a_2)
       
        self.label_valor_mayores_a_2 = tk.Label(self.ventana, text="0")
        label_img_mayores_a_2.pack( anchor='center', pady=5, side='right')
        self.label_valor_mayores_a_2.pack(anchor='center', pady=5, side='right')

        
        label_img_menores_a_2.pack( anchor='center', pady=5, side='right')
        self.label_valor_menores_a_2 = tk.Label(self.ventana, text="0")
        self.label_valor_menores_a_2.pack(anchor='center', pady=5,side='right')


        label_img_mayores_a_2.image = img_mayores_a_2  # Evitar que la imagen sea eliminada por el recolector de basura
        label_img_menores_a_2.image = img_menores_a_2

        # Actualizar el reloj cada segundo
        self.actualizar_reloj()
        # Agregar un Label para mostrar la hora actual
        self.hora_label = tk.Label(self.ventana, font=('calibri', 12), background='white', foreground='black')
        self.hora_label.pack(anchor='center', pady=10)
      
        icono_path = os.path.join(directorio_actual, "bar-graph.ico")  # Reemplaza con el nombre de tu icono
        self.ventana.iconbitmap(icono_path)
        

        self.figura, self.ax = Figure(), None
        label_texto.pack()
        correo.pack()
        self.inicializar_grafica()

        # Botón para cerrar la aplicación
        boton_cerrar = tk.Button(self.ventana, text="Cerrar", command=self.cerrar_ventana)
        boton_cerrar.pack()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)  # Manejar el evento de cerrar ventana

        self.ventana.mainloop()

    def inicializar_grafica(self):
        self.figura = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.ventana)
        self.canvas.get_tk_widget().pack()

        # Llamada recurrente para actualizar la gráfica cada 2 segundos
        self.actualizar_grafica()
    def actualizar_reloj(self):
        hora_actual = datetime.now().strftime('%H:%M:%S %p')

        # Actualizar el contenido del Label
        self.reloj_label.config(text=hora_actual)

        # Llamada recurrente cada 1000 milisegundos (1 segundo)
        self.ventana.after(1000, self.actualizar_reloj)   


    def agregar_numero(self, nuevo_numero):
        converted_val = 1 if float(nuevo_numero) > 2 else -1
        if float(nuevo_numero) > 2:
            self.num_mayores_a_2 += 1
            self.activar_cronometro()
        else:
            self.num_menores_a_2 += 1

        # Actualizar los Labels con los nuevos valores
        self.label_valor_mayores_a_2.config(text=str(self.num_mayores_a_2))
        self.label_valor_menores_a_2.config(text=str(self.num_menores_a_2))


        if len(self.serie_numeros) > 0:
            self.serie_numeros.append(self.serie_numeros[-1] + converted_val)
        else:
            self.serie_numeros.append(converted_val)

        if len(self.serie_numeros) > 100:
            self.serie_numeros.pop(0)
        #if float(nuevo_numero) > 3:
            # Actualizar el Label con la hora actual más 1.33 segundos
            #self.actualizar_label_con_hora()
   
    def actualizar_label_con_hora(self):
        # Obtener la hora actual
        hora_actual = datetime.now().strftime('%H:%M:%S')

        # Calcular la hora actual más 1.33 segundos
        nueva_hora = (datetime.now() + timedelta(minutes=1, seconds=33)).strftime('%H:%M:%S')

        # Actualizar el texto del Label
        mensaje = f"Nuevo número mayor a 3 a las {hora_actual}."
        self.hora_label.config(text=mensaje)

        # Llamada recurrente después de 1.33 segundos para borrar el mensaje
        #self.ventana.after(1330, self.borrar_label_con_hora)

   # def borrar_label_con_hora(self):
        # Borrar el texto del Label
        #self.hora_label.config(text="")

    def actualizar_grafica(self):
       #self.agregar_numero(np.random.uniform(0, 20))
        global resultado_final_check, resultado_final, historial_resultados
        if resultado_final != resultado_final_check:
            resultado_final_check=resultado_final
            if resultado_final:
                NuevoDato = float(resultado_final)
            
            else:
                print("La lista resultado_final está vacía.")

    
    
        #historial_resultados=resultado_final+historial_resultados
        #historial_resultados.append(float(resultado_final))
            historial_resultados.insert(0,float(resultado_final))
            
            os.system('cls')
        
    
            
            if len(historial_resultados) >= 1:
                print(historial_resultados[0])
            #agregar_numero(historial_resultados[0])
                self.agregar_numero(historial_resultados[0])
             
           
         
            else:
                print("Aun no hay 5 elementos.")
        
        self.ax.clear()
        self.ax.plot(self.serie_numeros, marker='*', color='blue')
        self.ax.set_title("Serie de Números")
        self.ax.set_xlabel("Índice")
        self.ax.set_ylabel("Valor")
        # Agregar línea horizontal para la media
        media = np.mean(self.serie_numeros)
        self.ax.axhline(y=media, color='red', linestyle='--', label='Media')
         # Graficar soportes y resistencias
      


        self.canvas.draw()

        # Llamada recurrente cada 2 segundos
        self.ventana.after(2000, self.actualizar_grafica)

    def cerrar_ventana(self):
        self.cerrar_navegador()
        self.ventana.destroy()
        
    def cerrar_navegador(self):
        # Cerrar el navegador aquí
        if self.driver:
            self.driver.quit()    

    def activar_cronometro(self):
        # Iniciar el cronómetro solo si no está activo
        if not self.cronometro_activo:
            self.tiempo_inicio_cronometro = datetime.now()
            self.cronometro_activo = True
            self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if self.cronometro_activo:
            tiempo_transcurrido = datetime.now() - self.tiempo_inicio_cronometro
            tiempo_restante = self.tiempo_restante - tiempo_transcurrido

            # Actualizar la visualización del cronómetro
            tiempo_formateado = tiempo_restante.total_seconds()
            self.hora_label.config(text=f"Cronómetro: {int(tiempo_formateado // 60):02d}:{int(tiempo_formateado % 60):02d}")

            # Verificar si el tiempo ha llegado a cero
            if tiempo_restante <= timedelta(seconds=0):
                self.cronometro_activo = False
                self.hora_label.config(text="Cronómetro: 00:00")
            else:
                # Llamada recurrente para actualizar el cronómetro cada 1000 milisegundos (1 segundo)
                self.ventana.after(1000, self.actualizar_cronometro)    
    def graficar_soportes_resistencias(self):
        if len(self.serie_numeros) > 2:
            # Encontrar máximos y mínimos
            indices_maximos = argrelextrema(np.array(self.serie_numeros), np.greater)[0]
            indices_minimos = argrelextrema(np.array(self.serie_numeros), np.less)[0]

            # Obtener valores de máximos y mínimos
            valores_maximos = [self.serie_numeros[i] for i in indices_maximos]
            valores_minimos = [self.serie_numeros[i] for i in indices_minimos]

            # Mostrar valores en la interfaz gráfica
            self.mostrar_valores(indices_maximos, valores_maximos, 'Maximos')
            self.mostrar_valores(indices_minimos, valores_minimos, 'Minimos')

            # Resaltar máximos y mínimos en la gráfica
            self.ax.scatter(indices_maximos, valores_maximos, color='red', marker='o', label='Maximos')
            self.ax.scatter(indices_minimos, valores_minimos, color='green', marker='o', label='Minimos')

    def mostrar_valores(self, indices, valores, tipo):
        for i, valor in zip(indices, valores):
            mensaje = f"{tipo} en índice {i}: {valor:.2f}"
            self.ax.annotate(mensaje, xy=(i, valor), xytext=(i + 5, valor + 5), arrowprops=dict(facecolor='black', shrink=0.05))



# Llamada a la función y retención del objeto del navegador
#navegador = iniciar_sesion_y_navegar2()
iniciar_sesion_desde_interfaz()
# Crear un hilo que ejecuta la función
thread = threading.Thread(target=ejecutora)
# Iniciar el hilo
thread.start()        
interfaz_grafica = InterfazGrafica()        