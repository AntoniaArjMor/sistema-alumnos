
"""!

@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).

"""

import os
from flask import Flask, jsonify, request


## Instancia principal de la aplicación Flask.
app = Flask(__name__)


## Base de datos en memoria (solo para fines de la actividad).
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]


## Versión de la aplicación inyectada por el pipeline Jenkins.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Genera un saludo personalizado.

    Obtiene el nombre desde el parámetro de consulta de la URL
    y devuelve un mensaje de bienvenida.

    @return Mensaje de saludo personalizado.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Comprueba el estado de la API.

    @return Respuesta JSON indicando que la aplicación está funcionando.
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Obtiene la versión actual de la aplicación.

    @return Respuesta JSON con el nombre de la aplicación y su versión.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Lista todos los alumnos registrados.

    @return Lista de alumnos en formato JSON.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Busca un alumno por su identificador.

    @param alumno_id Identificador numérico del alumno.
    @return Datos del alumno en JSON o error 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Registra un nuevo alumno.

    Valida que el nombre sea obligatorio y que el promedio
    sea un número entre 1.0 y 7.0.

    @return Datos del alumno creado con código 201,
            o mensaje de error con código 400.
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }

    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Inicia el servidor de desarrollo Flask.

    @return None.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()
