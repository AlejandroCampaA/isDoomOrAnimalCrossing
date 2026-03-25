# isDoomOrAnimalCrossing

Guia rapida para instalar, iniciar y usar la app que clasifica imagenes entre Doom y Animal Crossing.

## Que es esta app

Es una app web local hecha con Streamlit que carga un modelo de IA (.keras) y analiza imagenes para estimar si pertenecen a Doom o a Animal Crossing.

En la interfaz puedes:

- Subir una o varias imagenes al mismo tiempo.
- Ver probabilidades para ambas clases.
- Ver mensajes de confianza (alta, media, empate tecnico, etc.).
- Usar el modelo incluido por defecto o subir tu propio modelo .keras.

El proyecto ya incluye imagenes de prueba en la carpeta testImages, para validar rapido que todo funciona en local.

## 1. Requisitos

- Python 3.12 o menor.
- Recomendado: Python 3.12 exacto para evitar problemas de compatibilidad con TensorFlow.
- pip actualizado.
- Git y terminal.

Nota importante: TensorFlow no tiene soporte oficial para versiones nuevas de Python por encima de 3.12 en muchos entornos. Si usas Python 3.13+, la instalacion puede fallar.

## 2. Clonar el proyecto

Asumiendo que ya manejas Git y terminal:

	git clone https://github.com/AlejandroCampaA/isDoomOrAnimalCrossing.git
	cd isDoomOrAnimalCrossing

## 3. Crear entorno virtual (obligatorio)

### Windows (PowerShell)

Usa Python 3.12 de forma explicita:

	py -3.12 -m venv venv

Activar entorno:

	.\venv\Scripts\Activate.ps1

Si PowerShell bloquea scripts por politicas de ejecucion:

	Set-ExecutionPolicy -Scope Process Bypass
	.\venv\Scripts\Activate.ps1

### Linux

Usa Python 3.12 de forma explicita:

	python3.12 -m venv venv

Activar entorno:

	source venv/bin/activate

## 4. Instalar dependencias

Con el entorno virtual activo:

	python -m pip install --upgrade pip
	pip install -r requirements.txt

## 5. Iniciar la app

Con el entorno activo, ejecutar:

	streamlit run app.py

Al iniciar, Streamlit mostrara una URL local (normalmente http://localhost:8501) para abrir la interfaz.

## 6. Prueba rapida en local (recomendada)

1. Ejecuta la app con streamlit run app.py.
2. Abre la URL local que aparece en terminal.
3. Sube 2 o 3 imagenes desde la carpeta testImages.
4. Confirma que ves los porcentajes y el resultado por cada imagen.
5. Verifica en la barra lateral que esta usando el modelo por defecto modelo_doom_vs_ac.keras.

## 7. Uso rapido de la app

1. Abre la app en el navegador.
2. Verifica que cargue el modelo por defecto (modelo_doom_vs_ac.keras) o sube uno propio en la barra lateral.
3. Sube una o varias imagenes (.jpg, .jpeg, .png).
4. Revisa la prediccion y el nivel de confianza.

## 8. Reentrenar el modelo (trainer.py)

Si quieres crear un modelo nuevo desde cero, usa el archivo trainer.py.

Dataset (imagenes):
https://drive.google.com/drive/folders/14iT4mBdvX0x7XGf9lvRTZ4ANLwlS7GwN?usp=sharing

Pasos recomendados en local:

1. Descarga el dataset del enlace.
2. Organiza la carpeta como dataset_doom_animal con subcarpetas por clase (ejemplo: doom y animal_crossing).
3. Deja la carpeta dataset_doom_animal en la raiz del proyecto.
4. Ejecuta:

	python trainer.py

5. Al terminar, se generara un nuevo modelo_doom_vs_ac.keras.

Nota: trainer.py detecta Google Colab automaticamente, pero en modo local usa la ruta ./dataset_doom_animal.

## Preguntas frecuentes y errores comunes

### Error: No matching distribution found for tensorflow

Posible causa: version de Python incompatible.

Solucion:

- Verifica version: python --version
- Usa Python 3.12 o menor.
- Recrea el entorno virtual con Python 3.12:

	  py -3.12 -m venv venv

### Error al activar entorno en PowerShell

Posible causa: politica de ejecucion restringida.

Solucion:

	Set-ExecutionPolicy -Scope Process Bypass
	.\venv\Scripts\Activate.ps1

### Error: modelo_doom_vs_ac.keras no encontrado

Posible causa: el archivo no esta en la carpeta raiz del proyecto.

Solucion:

- Confirma que existe en la misma carpeta que app.py.
- O sube un archivo .keras manualmente desde la barra lateral de la app.

### El entrenamiento falla porque no encuentra imagenes

Posible causa: la ruta del dataset local no coincide con la esperada por trainer.py.

Solucion:

- Verifica que exista la carpeta dataset_doom_animal en la raiz del proyecto.
- Verifica que dentro haya subcarpetas por clase con imagenes.
- Si usas otra ruta, ajusta la variable base_dir en trainer.py.

### La app no abre en el navegador

Solucion:

- Revisa que Streamlit este corriendo sin errores en terminal.
- Abre manualmente la URL que muestra Streamlit.
- Si el puerto esta ocupado, ejecuta:

	  streamlit run app.py --server.port 8502

## Cierre

Para salir de la app: Ctrl + C en la terminal.

Para desactivar el entorno virtual:

	deactivate