# IS_Practica2

# 🚂 Sistema de Monitorización y Detección de Incidencias Ferroviarias

**Proyecto Grupal de Ingeniería del Software - Práctica 2**

Este proyecto implementa una solución de software completa para la detección, predicción y notificación de incidencias en vías de tren. El equipo ha diseñado una arquitectura distribuida que combina un **Backend en Python** (con Inteligencia Artificial) y un **Frontend Web** para la gestión de alertas en tiempo real.

---

## 🚀 Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Backend Web:** Flask (API REST)
* **Inteligencia Artificial:** Scikit-Learn (Random Forest Classifier)
* **Procesamiento de Datos:** Pandas, Numpy
* **Frontend:** HTML5, JavaScript (Fetch API), Chart.js
* **Gestión de Dependencias:** `requirements.txt`

---

## 🔄 Flujo de Ejecución Global (¿Cómo funciona todo unido?)

El sistema no son clases sueltas, sino un engranaje coordinado. Este es el camino que sigue la información dentro de nuestro programa:

1.  **Arranque:** Al ejecutar `app.py`, se despierta el **Controlador** (el cerebro).
2.  **Lectura:** El Controlador pide a la clase **Lectura** que cargue el fichero CSV. Aquí se transforman los datos crudos en información útil y se aplica *Data Augmentation* para enseñar a la IA casos de bloqueo.
3.  **Inteligencia:** El Controlador pasa esos datos al **DetectorIncidencia**. Este entrena un modelo de *Random Forest* y predice si hay problemas.
4.  **Generación de Alertas:** Si el Detector ve algo raro, instancia un objeto **Incidencia** (puede ser de tipo *Bloqueo* o *Voltaje*) y se lo devuelve al sistema.
5.  **Filtrado y Aviso:** El Controlador pasa la incidencia al **GestorSuscripciones**. Este módulo revisa la lista de **Suscriptores** (empleados) y decide a quién avisar según sus preferencias (Atributo `interes`).
6.  **Visualización:** Finalmente, la página web (**Cliente**) consulta al servidor mediante la API REST y pinta los gráficos y las alertas filtradas.

---

## 📘 Documentación Técnica de Clases

A continuación, detallamos la estructura interna de las clases desarrolladas por el equipo, especificando sus atributos y métodos clave.

### 1. El Núcleo de Control

#### `Controlador.py` (Patrón Controlador)
Es el orquestador que conecta la interfaz web con la lógica de negocio.
* **Atributos:**
    * `detector`: Instancia del motor de IA.
    * `gestor`: Instancia del sistema de notificaciones.
    * `df`: El DataFrame con los datos cargados en memoria.
* **Métodos:**
    * `cargar_datos()`: Lee el CSV y prepara el entorno.
    * `iniciar_sistema()`: Ejecuta el entrenamiento y la detección inicial.

#### `DetectorIncidencia.py` (Módulo IA)
Encapsula la lógica de Machine Learning.
* **Atributos:**
    * `modelo`: El algoritmo *RandomForestClassifier* configurado con balanceo de clases.
    * `cols_voltaje`: Lista de columnas del sensor a vigilar.
* **Métodos:**
    * `entrenar(df_train, df_test)`: Entrena la IA y devuelve los datos listos para el testing.
    * `detectar_incidencias(df)`: Predice fallos y fabrica objetos `Incidencia`.

### 2. Dominio de Datos e Incidencias

#### `Lectura.py`
Clase de utilidad para el manejo de datos crudos.
* **Métodos Estáticos:**
    * `leerCSV(ruta)`: Convierte el fichero de texto en un DataFrame de Pandas estructurado.

#### `Incidencia.py` (Clase Abstracta)
Plantilla base para cualquier error.
* **Atributos:** `hora`, `dispositivoAfectado`.
* **Métodos:** `describir_problema()` (Abstracto).

#### `IncidenciaBloqueo.py` (Hija)
Representa una parada de tren prolongada.
* **Atributos:** `duracion` (Segundos que el tren lleva parado).
* **Métodos:** `describir_problema()` -> Devuelve mensaje de "BLOQUEO CRÍTICO".

#### `IncidenciaVoltaje.py` (Hija)
Representa un fallo eléctrico.
* **Atributos:** `voltaje_leido`, `diferencia` (El salto de voltaje detectado).
* **Métodos:** `describir_problema()` -> Devuelve mensaje de "FALLO ELÉCTRICO".

### 3. Sistema de Notificaciones (Patrón Observer)

#### `GestorSuscripciones.py`
Gestiona la lista de interesados.
* **Atributos:** `subscriptores` (Lista de objetos Usuario).
* **Métodos:**
    * `suscribir(usuario)`: Añade a alguien a la lista.
    * `notificar_suscriptores(incidencia)`: Recorre la lista y avisa.

#### `SuscriptorConcreto.py`
Representa a un empleado real conectado al sistema.
* **Atributos:**
    * `nombre`: Nombre del operario (ej. "Juan").
    * `interes`: Filtro de alertas ("BLOQUEO", "VOLTAJE", o "TODO").
* **Métodos:**
    * `update(incidencia)`: Método que recibe la alerta del Gestor.

---

## ⚙️ Instrucciones de Instalación y Ejecución

Para ejecutar nuestro proyecto en cualquier máquina, sigue estos pasos:

1.  **Preparar el entorno:**
    Abre la terminal en la carpeta del proyecto.

2.  **Instalar dependencias:**
    Hemos generado un archivo con todas las librerías necesarias. Ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Arrancar el Servidor:**
    Lanza la aplicación web con el siguiente comando:
    ```bash
    python src/app.py
    ```

4.  **Acceder al Dashboard:**
    Abre tu navegador web y visita: `http://127.0.0.1:5000`

---

## 📊 Justificación de Decisiones de Diseño

Como equipo, hemos tomado las siguientes decisiones técnicas:

1.  **Arquitectura Cliente-Servidor:** Para cumplir con el requisito de "HTTP/REST", separamos la lógica Python (Backend) de la visualización HTML/JS (Frontend).
2.  **Uso de Patrones:**
    * **Observer:** Permite añadir suscriptores dinámicamente desde la web sin tocar el código del detector.
    * **Strategy:** Nos permite tratar los *Bloqueos* y *Voltajes* de forma polimórfica.
3.  **Data Augmentation:** Detectamos que el dataset original tenía un desbalanceo severo (los bloqueos solo aparecían en el Test). Implementamos una inyección de datos sintéticos en el entrenamiento para asegurar que el modelo aprendiera correctamente la clase minoritaria.