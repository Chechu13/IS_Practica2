from flask import Flask, jsonify, render_template, request
from sklearn.model_selection import train_test_split
from Controlador import Controlador
from IncidenciaBloqueo import IncidenciaBloqueo
from IncidenciaVoltaje import IncidenciaVoltaje
from SuscriptorConcreto import SubscriptorConcreto
from Dispositivo import Dispositivo

app = Flask(__name__)

sistema = Controlador()
print("--- SERVIDOR WEB INICIANDO ---")
sistema.cargar_datos()

df_train, df_test = train_test_split(sistema.df, test_size=0.20, shuffle=False)
sistema.detector.entrenar(df_train, df_test)
lista_incidencias_cache = sistema.detector.detectar_incidencias(df_test)

jefe = SubscriptorConcreto("Jefe Estación", interes="BLOQUEO")
sistema.gestor.suscribir(jefe)

print("--- SERVIDOR LISTO ---")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/datos')
def api_datos():
    datos_para_enviar = []
    usuarios_registrados = sistema.gestor.subscriptores

    for inc in lista_incidencias_cache:
        disp_real = Dispositivo(inc.dispositivoAfectado)
        nombre_dispositivo = disp_real.get_identificador_completo()

        tipo_incidencia = "DESCONOCIDO"
        avisados_nombres = []

        if isinstance(inc, IncidenciaBloqueo):
            tipo_incidencia = "BLOQUEO"
        elif isinstance(inc, IncidenciaVoltaje):
            tipo_incidencia = "VOLTAJE"

        for usuario in usuarios_registrados:
            if usuario.interes == "TODO" or usuario.interes == tipo_incidencia:
                avisados_nombres.append(usuario.nombre)

        dato = {
            "hora": str(inc.hora),
            "tipo": tipo_incidencia,
            "mensaje": f"[{nombre_dispositivo}] {inc.describir_problema()}",
            "notificados": avisados_nombres
        }
        datos_para_enviar.append(dato)

    return jsonify(datos_para_enviar)

@app.route('/api/suscribir', methods=['POST'])
def api_suscribir():
    datos = request.get_json()
    nombre = datos.get('nombre')
    interes = datos.get('interes')

    if nombre and interes:
        nuevo_usuario = SubscriptorConcreto(nombre, interes)
        sistema.gestor.suscribir(nuevo_usuario)

        print(f"NUEVO REGISTRO: {nombre} interesado en {interes}")
        return jsonify({"status": "ok", "msg": f"{nombre} suscrito a alertas de {interes}"}), 200

    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)