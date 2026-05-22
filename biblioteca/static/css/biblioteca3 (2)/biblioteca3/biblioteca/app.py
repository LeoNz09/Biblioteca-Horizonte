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


# ==========================================
# 1. PÁGINA DE INICIO PÚBLICA (INDEX)
# ==========================================
@app.route('/')
def inicio():
    # Abre directamente el index sin pedir login previo. 
    # El archivo index.html usará la sesión para saber si renderiza el menú normal o el de admin.
    return render_template('index.html')


# ==========================================
# 2. LOGIN ÚNICAMENTE PARA ADMINISTRADORES
# ==========================================
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


# ==========================================
# 3. MÓDULOS DEL MENÚ DE USUARIO NORMAL
# ==========================================
@app.route('/catalogo')
def catalogo():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('Catalogo.html', libros=libros)


@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():
    estado = None
    titulo_buscado = None
    
    if request.method == 'POST':
        accion = request.form.get('accion') 
        titulo_ingresado = request.form.get('titulo').strip() 
        titulo_buscado = titulo_ingresado 
        
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query_buscar = "SELECT id_libro, disponibles FROM libros WHERE titulo = %s"
        cursor.execute(query_buscar, (titulo_ingresado,))
        libro = cursor.fetchone()
        
        if accion == 'buscar':
            if not libro:
                estado = 'no_existe'    
            elif libro['disponibles'] <= 0:
                estado = 'no_disponible'    
            else:
                estado = 'existe' 

        elif accion == 'solicitar':
            if libro and libro['disponibles'] > 0:
                nueva_cantidad = libro['disponibles'] - 1
                query_actualizar = "UPDATE libros SET disponibles = %s WHERE id_libro = %s"
                cursor.execute(query_actualizar, (nueva_cantidad, libro['id_libro']))
                conexion.commit()   
                estado = 'prestado_con_exito'
            else:
                estado = 'no_disponible'
                
        cursor.close()
        conexion.close()
        
    return render_template('Prestamos.html', estado=estado, titulo_buscado=titulo_buscado)


@app.route('/devoluciones', methods=['GET', 'POST'])
def devoluciones():
    estado = None
    titulo_buscado = None
    
    if request.method == 'POST':
        accion = request.form.get('accion') 
        titulo_ingresado = request.form.get('titulo').strip()
        titulo_buscado = titulo_ingresado 
        
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query_buscar = "SELECT id_libro, disponibles, cantidad FROM libros WHERE titulo = %s"
        cursor.execute(query_buscar, (titulo_ingresado,))
        libro = cursor.fetchone()
        
        if accion == 'buscar':
            if not libro:
                estado = 'no_existe'    
            elif libro['disponibles'] >= libro['cantidad']:
                estado = 'completo' 
            else:
                estado = 'apto' 

        elif accion == 'devolver':
            if libro and libro['disponibles'] < libro['cantidad']:
                nueva_cantidad = libro['disponibles'] + 1
                query_actualizar = "UPDATE libros SET disponibles = %s WHERE id_libro = %s"
                cursor.execute(query_actualizar, (nueva_cantidad, libro['id_libro']))
                conexion.commit() 
                estado = 'devolucion_con_exito'
            else:
                estado = 'completo'
                
        cursor.close()
        conexion.close()
        
    return render_template('Devoluciones.html', estado=estado, titulo_buscado=titulo_buscado)


# ==========================================
# 4. MÓDULOS EXCLUSIVOS DE ADMINISTRADOR
# ==========================================
# MODULO PARA HISTORIAL
@app.route('/historial')
def historial():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM prestamo")

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("historial.html", prestamos=datos)



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


if __name__ == '__main__':
    app.run(debug=True)