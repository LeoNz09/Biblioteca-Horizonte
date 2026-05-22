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
    titulo_buscado = None

    if request.method == 'POST':
        accion = request.form.get('accion')     #boton de accion de buscar
        titulo_ingresado = request.form.get('titulo').strip()   # Limpiar espacios en blanco
        titulo_buscado = titulo_ingresado   #Mantener el texto

        # Abrir conexion con el servidor MySQL
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Consultar el libro
        query_buscar = "SELECT id_libro, disponibles FROM libros WHERE titulo = %s"
        cursor.execute(query_buscar, (titulo_ingresado,))
        libro = cursor.fetchone()   # Devuelve el registro encontrado

        # BUSCAR LIBRO
        if accion == 'buscar':
            if not libro:
                estado = 'no_existe'        # El libro no existe en la base de datos
            elif libro['disponibles'] <= 0:
                estado = 'no_disponible'    # El libro existe pero no hay copias disponibles
            else:
                estado = 'existe'           # El libro existe y hay copias disponibles

        # CONFIRMAR Y SOLICITAR PRESTAMO
        elif accion == 'solicitar':
            nombre_prestamista = request.form.get('nombre_prestamista', '').strip()

            if libro and libro['disponibles'] > 0 and nombre_prestamista:

                try:
                    # Disminuir el stock para el libro prestado
                    nueva_cantidad = libro['disponibles'] - 1
                    query_actualizar = "UPDATE libros SET disponibles = %s WHERE id_libro = %s"
                    cursor.execute(query_actualizar, (nueva_cantidad, libro['id_libro']))

                    # REGISTRAR EL PRESTAMO EN LA TABLA PRESTAMO
                    query_insertar = "INSERT INTO prestamo (titulo_libro, nombre_prestamista) VALUES (%s, %s)"
                    cursor.execute(query_insertar, (titulo_ingresado, nombre_prestamista))

                    # Confirmar operaciones en la base de datos
                    conexion.commit()
                    estado = 'prestado_con_exito'

                except mysql.connector.Error as err:
                    print(f"Error en la transaccion: {err}")
                    conexion.rollback()     # Cancela el prestamo si algo falla
                    estado = 'error_db'
            else:
                estado = 'no_disponible'

        # Cerrar flujos abiertos
        cursor.close()
        conexion.close()

    return render_template('Prestamos.html', estado=estado, titulo_buscado=titulo_buscado)

# MODULO PARA DEVOLUCIONES
@app.route('/devoluciones', methods=['GET', 'POST'])
def devoluciones():
    estado = None
    titulo_buscado = None
    
    if request.method == 'POST':
        accion = request.form.get('accion') # botón de buscar o devolver
        titulo_ingresado = request.form.get('titulo').strip()   #limpiar espacios en blanco
        titulo_buscado = titulo_ingresado # Mantiene el texto en la caja de búsqueda
        
        # Abrir conexion con el servidor MySQL
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # Buscar el libro en la base de datos y ver el stock del libro
        query_buscar = "SELECT id_libro, disponibles, cantidad FROM libros WHERE titulo = %s"
        cursor.execute(query_buscar, (titulo_ingresado,))
        libro = cursor.fetchone()   # Devuelve el registro encontrado
        
        # Buscar el libro en la base de datos
        if accion == 'buscar':
            if not libro:
                estado = 'no_existe'    # El libro no existe
            elif libro['disponibles'] >= libro['cantidad']:
                estado = 'completo'     # El libro existe pero ya están todas las copias
            else:
                estado = 'apto'         # El libro existe y hay copias pendientes por devolver

        # VALIDAR USUARIO Y CONFIRMAR LA DEVOLUCIÓN        
        elif accion == 'devolver':
            nombre_prestamista = request.form.get('nombre_prestamista', '').strip()
            
            # Validar que faltan copias del libro
            if libro and libro['disponibles'] < libro['cantidad']:
                
                # Validar que el usuario tenga un libro pendiente por devolver
                query_validar_prestamo = "SELECT id_prestamo FROM prestamo WHERE titulo_libro = %s AND nombre_prestamista = %s LIMIT 1"
                cursor.execute(query_validar_prestamo, (titulo_ingresado, nombre_prestamista))
                prestamo_activo = cursor.fetchone()
                
                if not prestamo_activo:
                    estado = 'usuario_incorrecto'  # El usuario no coincide con el préstamo de ese libro
                else:
                    try:
                        # Incrementar el stock disponible en la tabla de "libros"
                        nueva_cantidad = libro['disponibles'] + 1
                        query_actualizar = "UPDATE libros SET disponibles = %s WHERE id_libro = %s"
                        cursor.execute(query_actualizar, (nueva_cantidad, libro['id_libro']))
                        
                        # Registrar el movimiento en la tabla de "devolucion"
                        query_insertar_devolucion = "INSERT INTO devolucion (titulo_libro, nombre_prestamista) VALUES (%s, %s)"
                        cursor.execute(query_insertar_devolucion, (titulo_ingresado, nombre_prestamista))
                        
                        # Eliminar al usuario de la tabla "prestamo"
                        query_eliminar_prestamo = "DELETE FROM prestamo WHERE id_prestamo = %s"
                        cursor.execute(query_eliminar_prestamo, (prestamo_activo['id_prestamo'],))
                        
                        # Confirmar todas las operaciones realizadas
                        conexion.commit() 
                        estado = 'devolucion_con_exito'
                    except mysql.connector.Error as err:
                        print(f"Error en la transacción de devolución: {err}")
                        conexion.rollback() # Cancela la devolucion si algo falla
                        estado = 'error_db'
            else:
                estado = 'completo'
                
        # Cerrar flujos abiertos        
        cursor.close()
        conexion.close()
        
    return render_template('Devoluciones.html', estado=estado, titulo_buscado=titulo_buscado)


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

if __name__ == '__main__':
    app.run(debug=True)