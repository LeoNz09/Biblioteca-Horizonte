print("APP CARGADA CORRECTAMENTE")
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# LLAVE SECRETA: Requerida por Flask para manejar las sesiones del Administrador
app.secret_key = 'clave_secreta_horizonte_biblioteca'

# Configuración para hacer la conexión con MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',       # El usuario por defecto root
    'password': '',       
    'database': 'biblio_horizonte_1'
}

# Abrir y retornar una conexión a la base de datos
def obtener_conexion():
    return mysql.connector.connect(**db_config)


# PÁGINA DE INICIO (INDEX)

@app.route('/')
def inicio():
    # Abre directamente el index sin pedir login previo. 
    # El archivo index.html usará la sesión para saber si renderiza el menú normal o el de admin.
    return render_template('index.html')


# -- LOGIN ÚNICAMENTE PARA ADMINISTRADORES --

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        correo = request.form.get('correo').strip()
        contrasena = request.form.get('contrasena').strip()

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Validación directa con la tabla 'administradores' de tu SQL
        query = "SELECT * FROM administradores WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, (correo, contrasena))
        admin = cursor.fetchone()

        cursor.close()
        conexion.close()

        if admin:
            # Se guardan los datos en la sesión para reconocerlo como Administrador
            session['admin_id'] = admin['id_admin']
            session['nombre'] = admin['nombre']
            session['rol'] = 'administrador'
            return redirect(url_for('inicio'))
        else:
            error = "Credenciales de Administrador incorrectas."

    return render_template('login.html', error=error)


# CERRAR SESIÓN DE ADMINISTRADOR
@app.route('/logout')
def logout():
    session.clear() # Limpia la sesión y vuelve a ser un usuario normal
    return redirect(url_for('inicio'))


# -- MÓDULOS DEL MENÚ DE USUARIO NORMAL --

# MODULO PARA EL CATALOGO
@app.route('/catalogo')
def catalogo():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('Catalogo.html', libros=libros)

# MODULO PARA PRESTAMOS 
@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():

    estado = None
    libros_prestados = []
    libros_catalogo = []
    estudiante_valido = False
    matricula = ""

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # =========================
    # POST
    # =========================
    if request.method == 'POST':

        accion = request.form.get('accion')
        matricula = request.form.get('matricula', '').strip()

        # =========================
        # VALIDAR ESTUDIANTE
        # =========================
        cursor.execute("""
            SELECT nombre, apellidos
            FROM estudiantes
            WHERE matricula = %s
        """, (matricula,))

        estudiante = cursor.fetchone()

        if not estudiante:
            estado = 'estudiante_no_existe'
            estudiante_valido = False

        else:
            estudiante_valido = True

            nombre_completo = estudiante['nombre'] + " " + estudiante['apellidos']

            # =========================
            # CATALOGO FILTRADO
            # =========================
            cursor.execute("""
                SELECT id_libro, titulo, autor, categoria, descripcion, disponibles
                FROM libros l
                WHERE l.disponibles > 0
                AND l.titulo NOT IN (
                    SELECT p.titulo_libro
                    FROM prestamo p
                    WHERE p.matricula = %s
                )
            """, (matricula,))

            libros_catalogo = cursor.fetchall()

            # =========================
            # PRESTAMO
            # =========================
            if accion == 'solicitar':

                libros_ids = request.form.getlist('libros')

                if len(libros_ids) == 0:
                    estado = 'no_disponible'

                else:

                    try:

                        for libro_id in libros_ids:

                            # obtener libro
                            cursor.execute("""
                                SELECT id_libro, titulo, disponibles
                                FROM libros
                                WHERE id_libro = %s
                            """, (libro_id,))

                            libro = cursor.fetchone()

                            if not libro:
                                continue

                            # validar disponibilidad
                            if libro['disponibles'] <= 0:
                                continue

                            # validar duplicado
                            cursor.execute("""
                                SELECT id_prestamo
                                FROM prestamo
                                WHERE matricula = %s AND titulo_libro = %s
                            """, (matricula, libro['titulo']))

                            ya_prestado = cursor.fetchone()

                            if ya_prestado:
                                continue

                            # actualizar stock
                            cursor.execute("""
                                UPDATE libros
                                SET disponibles = disponibles - 1
                                WHERE id_libro = %s
                            """, (libro_id,))

                            # insertar prestamo
                            cursor.execute("""
                                INSERT INTO prestamo
                                (matricula, titulo_libro, nombre_prestamista)
                                VALUES (%s, %s, %s)
                            """, (
                                matricula,
                                libro['titulo'],
                                nombre_completo
                            ))

                            libros_prestados.append(libro['titulo'])

                        conexion.commit()
                        estado = 'prestado_con_exito'

                    except mysql.connector.Error as err:
                        print(err)
                        conexion.rollback()
                        estado = 'error_db'

    cursor.close()
    conexion.close()

    return render_template(
        'Prestamos.html',
        estado=estado,
        libros_catalogo=libros_catalogo,
        libros_prestados=libros_prestados,
        estudiante_valido=estudiante_valido,
        matricula=matricula
    )
##DEVOLUCIONESSS
@app.route('/devoluciones', methods=['GET', 'POST'])
def devoluciones():

    estado = None
    matricula = ""
    libros_usuario = []
    libros_devueltos = []
    libros_invalidos = []

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':

        accion = request.form.get('accion')
        matricula = request.form.get('matricula', '').strip()

        # =========================
        # VALIDAR SI EXISTE USUARIO
        # =========================
        cursor.execute("""
            SELECT DISTINCT matricula
            FROM prestamo
            WHERE matricula = %s
        """, (matricula,))

        usuario = cursor.fetchone()

        if not usuario:
            estado = 'usuario_no_existe'

        else:

            # =========================
            # PASO 1: BUSCAR LIBROS
            # =========================
            if accion == 'buscar':

                cursor.execute("""
                    SELECT id_prestamo, titulo_libro
                    FROM prestamo
                    WHERE matricula = %s
                """, (matricula,))

                libros_usuario = cursor.fetchall()

                if not libros_usuario:
                    estado = 'sin_prestamos'
                else:
                    estado = 'mostrar_libros'


            # =========================
            # PASO 2: DEVOLVER LIBROS
            # =========================
            elif accion == 'devolver':

                libros_ids = request.form.getlist('libros')

                if not matricula or len(libros_ids) == 0:
                    estado = 'error'

                else:
                    try:

                        for libro_id in libros_ids:

                            cursor.execute("""
                                SELECT id_prestamo, titulo_libro
                                FROM prestamo
                                WHERE id_prestamo = %s AND matricula = %s
                            """, (libro_id, matricula))

                            prestamo = cursor.fetchone()

                            if prestamo:

                                titulo = prestamo['titulo_libro']

                                cursor.execute("""
                                    UPDATE libros
                                    SET disponibles = disponibles + 1
                                    WHERE titulo = %s
                                """, (titulo,))

                                cursor.execute("""
                                    INSERT INTO devolucion
                                    (matricula, titulo_libro, nombre_prestamista)
                                    VALUES (%s, %s, %s)
                                """, (
                                    matricula,
                                    titulo,
                                    matricula
                                ))

                                cursor.execute("""
                                    DELETE FROM prestamo
                                    WHERE id_prestamo = %s
                                """, (libro_id,))

                                libros_devueltos.append(titulo)

                            else:
                                libros_invalidos.append(libro_id)

                        conexion.commit()
                        estado = 'devolucion_ok'

                    except mysql.connector.Error as err:
                        print("ERROR:", err)
                        conexion.rollback()
                        estado = 'error_db'

    cursor.close()
    conexion.close()

    return render_template(
        "Devoluciones.html",
        estado=estado,
        matricula=matricula,
        libros_usuario=libros_usuario,
        libros_devueltos=libros_devueltos,
        libros_invalidos=libros_invalidos
    )
# -- MÓDULOS EXCLUSIVOS DEL ADMINISTRADOR --

# MODULO PARA HISTORIAL
@app.route('/historial')
@app.route('/historial')
def historial():

    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT id_prestamo, titulo_libro, nombre_prestamista
    FROM prestamo
    """

    cursor.execute(query)

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'historial.html',
        datos=datos
    )

# MODULO PARA EL REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Seguridad: Si no es admin, rebota la solicitud
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    estado = None
    if request.method == 'POST':
        titulo = request.form.get('titulo').strip()
        autor = request.form.get('autor').strip()
        categoria = request.form.get('categoria').strip()
        isbn = request.form.get('isbn').strip()
        cantidad = int(request.form.get('cantidad'))

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            query_insertar = """
                INSERT INTO libros (titulo, autor, categoria, isbn, cantidad, disponibles)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insertar, (titulo, autor, categoria, isbn, cantidad, cantidad))
            conexion.commit()
            
            estado = 'exito'
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error en SQL: {err}")
            estado = 'error'

    return render_template('registro.html', estado=estado)

# MODULO PARA BUSCAR LIBROS 
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():

    libros = []

    if request.method == 'POST':

        texto = request.form.get('texto')

        conexion = obtener_conexion()

        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT *
        FROM libros
        WHERE titulo LIKE %s
        """

        cursor.execute(query, ('%' + texto + '%',))

        libros = cursor.fetchall()

        cursor.close()
        conexion.close()

    return render_template(
        'buscar.html',
        libros=libros
    )

@app.route('/detalle/<int:id_libro>')
def detalle(id_libro):

    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    query = """
    SELECT *
    FROM libros
    WHERE id_libro = %s
    """

    cursor.execute(query, (id_libro,))

    libro = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        'detalle.html',
        libro=libro
    )

# MODULO PARA DAR DE BAJA LIBROS (EXCLUSIVO ADMIN)
@app.route('/baja', methods=['GET', 'POST'])
def baja():
    # FILTRO DE SEGURIDAD: Si no es administrador, redirige al login de inmediato
    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    estado = None
    titulo_buscado = None
    libro = None

    if request.method == 'POST':
        accion = request.form.get('accion')
        titulo_ingresado = request.form.get('titulo').strip()
        titulo_buscado = titulo_ingresado

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Buscar si el libro existe en el catálogo general
        query_buscar = "SELECT id_libro, titulo, autor, cantidad FROM libros WHERE titulo = %s"
        cursor.execute(query_buscar, (titulo_ingresado,))
        libro = cursor.fetchone()

        # FASE 1: BUSCAR EL LIBRO A ELIMINAR
        if accion == 'buscar':
            if not libro:
                estado = 'no_existe'  # El libro no se encuentra en el inventario
            else:
                estado = 'existe'     # El libro fue localizado y muestra sus datos de confirmación

        # FASE 2: CONFIRMAR LA ELIMINACIÓN PERMANENTE
        elif accion == 'eliminar':
            if libro:
                try:
                    # Ejecutar la eliminación del registro usando su llave primaria
                    query_eliminar = "DELETE FROM libros WHERE id_libro = %s"
                    cursor.execute(query_eliminar, (libro['id_libro'],))
                   
                    # Consolidar de manera permanente el cambio en MySQL
                    conexion.commit()
                    estado = 'eliminado_con_exito'
                    libro = None  # Limpia la variable tras borrarlo
                except mysql.connector.Error as err:
                    print(f"Error al eliminar en la BD: {err}")
                    conexion.rollback()
                    estado = 'error_db'
            else:
                estado = 'no_existe'

        cursor.close()
        conexion.close()

    return render_template('baja.html', estado=estado, titulo_buscado=titulo_buscado, libro=libro)

# MÓDULO PARA REGISTRO DE ESTUDIANTES
@app.route('/registro_estudiantes', methods=['GET', 'POST'])
def registro_estudiantes():

    if 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('login'))

    estado = None

    if request.method == 'POST':

        nombre = request.form.get(
            'nombre'
        ).strip()

        apellidos = request.form.get(
            'apellidos'
        ).strip()

        matricula = request.form.get(
            'matricula'
        ).strip()

        carrera = request.form.get(
            'carrera'
        ).strip()

        # CREAR CORREO AUTOMATICO
        correo = matricula + "@biblio.com"

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            dictionary=True,
            buffered=True
        )

        # VALIDAR SI YA EXISTE LA MATRICULA
        query_validar = """
        SELECT *
        FROM estudiantes
        WHERE matricula = %s
        """

        cursor.execute(
            query_validar,
            (matricula,)
        )

        estudiante = cursor.fetchone()

        if estudiante:

            estado = 'matricula_repetida'

        else:

            try:

                query_insertar = """
                INSERT INTO estudiantes
                (
                    nombre,
                    apellidos,
                    matricula,
                    carrera,
                    correo
                )
                VALUES (%s, %s, %s, %s, %s)
                """

                cursor.execute(
                    query_insertar,
                    (
                        nombre,
                        apellidos,
                        matricula,
                        carrera,
                        correo
                    )
                )

                conexion.commit()

                estado = 'exito'

            except mysql.connector.Error as err:

                print(err)

                conexion.rollback()

                estado = 'error_db'

        cursor.close()
        conexion.close()

    return render_template(
        'registro_estudiantes.html',
        estado=estado
    )

if __name__ == '__main__':
    app.run(debug=True)