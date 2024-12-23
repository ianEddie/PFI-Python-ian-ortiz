import sqlite3

def connect_db():
    """Conectar o crear la base de datos."""
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit()
    return conn

def registrar_producto(conn):
    """Registrar un nuevo producto."""
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    cantidad = int(input("Cantidad inicial: "))
    precio = float(input("Precio: "))
    categoria = input("Categoría: ")

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
        (nombre, descripcion, cantidad, precio, categoria)
    )
    conn.commit()
    print("\nProducto registrado con éxito.\n")

def consultar_producto(conn):
    """Consultar detalles de un producto."""
    nombre = input("Nombre del producto a consultar: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
    producto = cursor.fetchone()
    if producto:
        print("\nDetalle del producto:")
        print(f"ID: {producto[0]}\nNombre: {producto[1]}\nDescripción: {producto[2]}\nCantidad: {producto[3]}\nPrecio: ${producto[4]}\nCategoría: {producto[5]}\n")
    else:
        print("\nProducto no encontrado.\n")

def actualizar_producto(conn):
    """Actualizar la cantidad disponible de un producto."""
    nombre = input("Nombre del producto a actualizar: ")
    nueva_cantidad = int(input("Nueva cantidad: "))

    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
    if cursor.rowcount > 0:
        conn.commit()
        print("\nCantidad actualizada con éxito.\n")
    else:
        print("\nProducto no encontrado.\n")

def eliminar_producto(conn):
    """Eliminar un producto del inventario."""
    nombre = input("Nombre del producto a eliminar: ")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
    if cursor.rowcount > 0:
        conn.commit()
        print("\nProducto eliminado con éxito.\n")
    else:
        print("\nProducto no encontrado.\n")

def listar_productos(conn):
    """Listar todos los productos del inventario."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("\nListado completo del inventario:")
    for producto in productos:
        print(f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[3]} | Precio: ${producto[4]} | Categoría: {producto[5]}")
    print()

def reporte_bajo_stock(conn):
    """Generar un reporte de productos con bajo stock."""
    limite = int(input("Ingresar el límite de stock bajo: "))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    print("\nReporte de productos con bajo stock:")
    if productos:
        for producto in productos:
            print(f"ID: {producto[0]} | Nombre: {producto[1]} | Cantidad: {producto[3]} | Categoría: {producto[5]}")
    else:
        print("No hay productos con bajo stock.")
    print()

def main():
    """Función principal para ejecutar el programa."""
    conn = connect_db()

    while True:
        print("\n=== Gestión de Inventario ===")
        print("1. Registrar producto")
        print("2. Consultar producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Listado completo")
        print("6. Reporte de bajo stock")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_producto(conn)
        elif opcion == "2":
            consultar_producto(conn)
        elif opcion == "3":
            actualizar_producto(conn)
        elif opcion == "4":
            eliminar_producto(conn)
        elif opcion == "5":
            listar_productos(conn)
        elif opcion == "6":
            reporte_bajo_stock(conn)
        elif opcion == "7":
            conn.close()
            print("\nSaliendo del programa.\n")
            break
        else:
            print("\nOpción no válida. Intenta nuevamente.\n")

if __name__ == "__main__":
    main()
