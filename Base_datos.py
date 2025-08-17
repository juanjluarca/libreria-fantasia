import pymysql
from pymysql import cursors

class BaseDatos:
    def __init__(self, user, password):
        self.conexion = pymysql.connect(
            # host="192.168.250.103",
            # user='pancho',
            # password='Pancho123?',
            host="localhost",
            user=user,
            password=password,
            database="modelo_proyecto",
            cursorclass=cursors.DictCursor
        )

    # =======================
    # MÉTODOS DE USUARIOS
    # =======================

    def agregar_usuario(self, nombre, email, tipo, contrasennia, telefono):
        # Agregar usuario nuevo
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO empleado (nombre, email, tipo, contrasennia, telefono)
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, email, tipo, contrasennia, telefono))
        self.conexion.commit()

    def modificar_usuario(self, id, nombre, email, tipo, contrasennia, telefono):
        # Modificar datos del usuario
        with self.conexion.cursor() as cursor:
            sql = """UPDATE empleado 
                    SET nombre = %s, email = %s, tipo = %s, contrasennia = %s, telefono = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (nombre, email, tipo, contrasennia, telefono, id))
        self.conexion.commit()

    def eliminar_usuario(self, id):
        # Eliminar usuario (lógica: cambiar estado)
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE empleado SET estado = %s WHERE id = %s", (0, id))
        self.conexion.commit()

    def obtener_usuarios(self):
        # Obtener todos los usuarios activos
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, email, tipo, telefono, estado FROM empleado WHERE estado = 1")
            return cursor.fetchall()

    def buscar_usuario_por_nombre(self, nombre):
        # Buscar usuarios por nombre
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT id, nombre, email, tipo, telefono 
                            FROM empleado 
                            WHERE nombre LIKE %s AND estado = 1""", (f"%{nombre}%",))
            return cursor.fetchall()

    def obtener_id_usuario(self, usuario):
        # Obtener ID del usuario
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM empleado WHERE nombre = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado['id'] if resultado else None

    def obtener_contraseña(self, usuario):
        # Obtener contraseña del usuario
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT contrasennia FROM empleado WHERE nombre = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado['contrasennia'] if resultado else None

    def obtener_nivel_usuario(self, usuario):
        # Obtener nivel/tipo del usuario
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT tipo FROM empleado WHERE nombre = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado['tipo'] if resultado else None

    # =======================
    # MÉTODOS DE PRODUCTOS
    # =======================

    def agregar_producto(self, nombre, precio, descripcion, existencia_minima):
        # Agregar producto nuevo
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO modelo_proyecto.producto 
                    (nombre, precio, descripcion, costo, stock_minimo) 
                    VALUES (%s, %s, %s, %s, %s)"""
            costo = precio - (precio * 0.15)
            cursor.execute(sql, (nombre, precio, descripcion, costo, existencia_minima))
        self.conexion.commit()

    def obtener_productos(self):
        # Obtener productos para administración
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT id, nombre, stock, precio, descripcion, costo, stock_minimo 
                            FROM modelo_proyecto.producto WHERE estado = 1""")
            return cursor.fetchall()

    def obtener_productos_ventas(self):
        # Obtener productos para ventas
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT id, nombre, stock, precio, descripcion 
                            FROM modelo_proyecto.producto WHERE estado = 1""")
            return cursor.fetchall()

    def buscar_producto_por_nombre(self, nombre):
        # Buscar productos para administración
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT id, nombre, stock, precio, descripcion, costo, stock_minimo 
                            FROM modelo_proyecto.producto 
                            WHERE nombre LIKE %s AND estado = 1""", (f"%{nombre}%",))
            return cursor.fetchall()

    def buscar_producto_ventas_por_nombre(self, nombre):
        # Buscar productos para ventas
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT id, nombre, descripcion, stock, precio 
                            FROM modelo_proyecto.producto 
                            WHERE nombre LIKE %s AND estado = 1""", (f"%{nombre}%",))
            return cursor.fetchall()

    def modificar_producto(self, id, nombre, precio, descripcion, existencia_minima):
        # Modificar datos de producto
        with self.conexion.cursor() as cursor:
            sql = """UPDATE producto 
                    SET nombre = %s, precio = %s, descripcion = %s, stock_minimo = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (nombre, precio, descripcion, existencia_minima, id))
        self.conexion.commit()

    def eliminar_producto(self, id):
        # Eliminar producto (cambiar estado)
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE producto SET estado = %s WHERE id = %s", (0, id))
        self.conexion.commit()

    def modificar_producto_stock(self, id, stock):
        # Modificar stock del producto
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE producto SET stock = %s WHERE id = %s", (stock, id))
        self.conexion.commit()

    def modificar_stock_producto(self, id, stock):
        # Otra variante para modificar stock
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE modelo_proyecto.producto SET stock = %s WHERE id = %s", (stock, id))
        self.conexion.commit()

    def aumentar_stock_producto(self, id, cantidad):
        # Aumentar stock de producto
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE modelo_proyecto.producto SET stock = stock + %s WHERE id = %s", (cantidad, id))
        self.conexion.commit()

    def obtener_stock_producto(self, id):
        # Obtener stock actual de producto
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT stock FROM modelo_proyecto.producto WHERE id = %s", (id,))
            resultado = cursor.fetchone()
            return resultado['stock'] if resultado else None

    # =======================
    # MÉTODOS DE COMPRAS
    # =======================

    def agregar_compra(self, proveedor_id, fecha, empleado_id, total_compra):
        # Registrar compra
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO compra (Proveedor_id, fecha, Empleado_id, total_compra) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (proveedor_id, fecha, empleado_id, total_compra))
            return cursor.lastrowid
        self.conexion.commit()

    def confirmar_orden_compra(self, id):
        # Confirmar orden de compra (cambiar estado)
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE compra SET estado = %s WHERE id = %s", (1, id))
        self.conexion.commit()

    def obtener_compras_pendientes(self):
        # Obtener compras pendientes (sin registrar en stock)
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT c.id as IdCompra, p.nombre as Proveedor, c.fecha as Fecha, c.total_compra as Total 
                            FROM compra c
                            JOIN proveedor p ON c.Proveedor_id = p.id
                            WHERE c.estado = 0 ORDER BY c.fecha DESC""")
            return cursor.fetchall()

    def agregar_detalle_compra(self, producto_id, compra_id, cantidad, precio, cantidad_recibida):
        # Agregar detalle a la compra
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO detalle_compra (Producto_id, Compra_id, cantidad, precio_unitario, cantidad_recibida) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (producto_id, compra_id, cantidad, precio, cantidad_recibida))
        self.conexion.commit()

    def obtener_detalle_compra(self, id):
        # Obtener detalle de una compra específica
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT dc.id as ID, dc.Producto_id as IdProducto, p.nombre as NombreProducto, 
                                    dc.precio_unitario as PrecioUnitario, dc.cantidad as Cantidad, dc.cantidad_recibida as CantidadRecibida
                            FROM detalle_compra dc
                            JOIN producto p ON dc.Producto_id = p.id
                            WHERE dc.Compra_id = %s""", (id,))
            return cursor.fetchall()
        
    def modificar_detalle_compra(self, id, cantidad_recibida):
        with self.conexion.cursor() as cursor:
            cursor.callproc("ModificarDetalleCompra", (id, cantidad_recibida))
        self.conexion.commit()


    # =======================
    # MÉTODOS DE VENTAS
    # =======================

    def agregar_venta(self, empleado_id, fecha, total_venta):
        # Registrar venta
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO venta (Empleado_id, fecha, total_venta) 
                    VALUES (%s, %s, %s)"""
            cursor.execute(sql, (empleado_id, fecha, total_venta))
        self.conexion.commit()

    def agregar_detalle_venta(self, producto_id, venta_id, cantidad, precio):
        # Agregar detalle a la venta
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO detalle_venta (Producto_id, Venta_id, cantidad, precio) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (producto_id, venta_id, cantidad, precio))
        self.conexion.commit()

    def obtener_id_ultima_venta(self):
        # Obtener el ID de la última venta registrada
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM venta ORDER BY id DESC LIMIT 1")
            resultado = cursor.fetchone()
            return resultado['id'] if resultado else None

    # =======================
    # MÉTODOS DE PROVEEDORES
    # =======================

    def obtener_proveedores(self):
        # Obtener proveedores activos
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, direccion, email, telefono FROM proveedor WHERE estado = 1")
            return cursor.fetchall()
        
    def obtener_id_nombre_proveedor(self):
        # Obtener ID y nombre de proveedores
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM proveedor WHERE estado = 1")
            return cursor.fetchall()

    def agregar_proveedor(self, nombre, direccion, email, telefono):
        # Agregar proveedor nuevo
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO proveedor (nombre, direccion, email, telefono) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, direccion, email, telefono))
        self.conexion.commit()

    def editar_proveedor(self, id, nombre, direccion, email, telefono): #  nombre, direccion, email, telefono
        # Editar proveedor
        with self.conexion.cursor() as cursor:
            sql = """UPDATE proveedor 
                    SET nombre = %s, direccion = %s, email = %s, telefono = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (nombre, direccion, email, telefono, id))
        self.conexion.commit()

    def eliminar_proveedor(self, id):
        # Eliminar proveedor (cambiar estado)
        with self.conexion.cursor() as cursor:
            cursor.execute("UPDATE proveedor SET estado = %s WHERE id = %s", (0, id))
        self.conexion.commit()


    # =======================
    # MÉTODOS DE REPORTES
        # =======================
    def obtener_reporte_ventas_por_producto(self, fecha_inicio, fecha_fin):
        """
        Devuelve una lista de productos vendidos entre dos fechas con su cantidad total y total generado.
        """
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.id AS IdProducto,
                    p.nombre AS Producto,
                    SUM(dv.cantidad) AS CantidadVendida,
                    p.precio AS PrecioUnitario,
                    SUM(dv.cantidad * p.precio) AS TotalGenerado
                FROM 
                    venta v
                    INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                    INNER JOIN producto p ON p.id = dv.Producto_id
                WHERE 
                    DATE(v.fecha) BETWEEN %s AND %s
                GROUP BY p.id
                ORDER BY CantidadVendida DESC
            """, (fecha_inicio, fecha_fin))

        return cursor.fetchall()
    def obtener_ventas_dia(self, fecha): # Devolver IdVenta, Producto, Cantidad, Precio
        # Obtener los productos vendidos en un día
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                p.id AS IdVenta, 
                                p.nombre AS Producto, 
                                sum(dv.cantidad) AS Cantidad, 
                                p.precio AS Precio
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON p.id = dv.Producto_id
                            WHERE 
                                DATE(v.fecha) = %s
                            group by p.id
                            order by sum(dv.cantidad) desc
                            """, (fecha,))
                            
            return cursor.fetchall()
        
    def obtener_ventas_mes(self, fecha):  # fecha esperada: 'YYYY-MM'
        # Obtener los productos vendidos en un mes
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.id AS IdVenta, 
                    p.nombre AS Producto, 
                    sum(dv.cantidad) AS Cantidad, 
                    p.precio AS Precio
                FROM 
                    venta v
                    INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                    INNER JOIN producto p ON p.id = dv.Producto_id
                WHERE 
                    DATE_FORMAT(v.fecha, '%%Y-%%m') = %s
                group by p.id
                order by sum(dv.cantidad) desc
            """, (fecha,))
            return cursor.fetchall()


    def obtener_reporte_ventas(self): # Devolver IdVenta, Empleado, Fecha, Total
        with self.conexion.cursor() as cursor:
            cursor.execute("""select 
                                v.id as IdVenta, 
                                e.nombre as Empleado, 
                                v.fecha as Fecha, 
                                v.total_venta as Total 
                            from 
                                empleado e 
                                inner join venta v on e.id = v.Empleado_id 
                            group by v.id
                            order by v.fecha desc""")
            return cursor.fetchall()
        
    def obtener_detalles_por_id_venta(self, id_venta): # Devolver IdOrden, Producto, CantidadVendida, Total 
        # Obtener detalles de una venta específica
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                dv.id AS IdOrden, 
                                p.nombre AS Producto, 
                                dv.cantidad AS CantidadVendida, 
                                dv.precio AS Total
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON p.id = dv.Producto_id
                            WHERE 
                                v.id = %s
                            GROUP BY 
                                dv.id""", (id_venta,))
            return cursor.fetchall()
        

    def obtener_reporte_ventas_por_fecha(self, fecha_inicio, fecha_fin): # Devuelve Fecha, IngresoTotal, ProductosVendidos, Ganancia
        # Obtener reporte de ventas por fecha
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE(v.fecha) AS Fecha,
                                SUM(v.total_venta) AS IngresoTotal,
                                SUM(dv.cantidad) AS ProductosVendidos,
                                SUM(v.total_venta) * 0.15 AS Ganancia
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON dv.Producto_id = p.id
                            WHERE 
                                DATE(v.fecha) BETWEEN %s AND %s
                            GROUP BY 
                                DATE(v.fecha)
                            ORDER BY 
                                Fecha DESC""", (fecha_inicio, fecha_fin))
            return cursor.fetchall()


    def obtener_reporte_ventas_por_dia(self): # select date(v.fecha) as Fecha, sum(v.total_venta) as IngresoTotal, sum(dv.cantidad) as ProductosVendidos, sum(v.total_venta) - sum(v.total_venta) * 0.15 as Ganancia, (select p2.nombre from producto p2 inner join detalle_venta dv2 on p2.id = dv.Producto_id group by p2.nombre order by sum(dv2.cantidad) desc limit 1) as Producto from producto p inner join detalle_venta dv on p.id = dv.Producto_id inner join venta v on v.id = dv.Venta_id group by date(v.fecha);
        # Obtener reporte de ventas
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE(v.fecha) AS Fecha,
                                SUM(dv.cantidad * dv.precio) AS IngresoTotal,
                                SUM(dv.cantidad) AS ProductosVendidos,
                                SUM(dv.cantidad * dv.precio) * 0.15 AS Ganancia
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON dv.Producto_id = p.id
                            GROUP BY 
                                DATE(v.fecha)
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_reporte_ventas_por_mes(self):
        # Obtener reporte de ventas por mes
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE_FORMAT(v.fecha, '%Y-%m') AS Fecha,
                                SUM(dv.cantidad * dv.precio) AS IngresoTotal,
                                SUM(dv.cantidad) AS ProductosVendidos,
                                SUM(dv.cantidad * dv.precio) * 0.15 AS Ganancia
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON dv.Producto_id = p.id
                            GROUP BY 
                                DATE_FORMAT(v.fecha, '%Y-%m')
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_reporte_ventas_por_anio(self):
        # Obtener reporte de ventas por año
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE_FORMAT(v.fecha, '%Y') AS Fecha,
                                SUM(dv.cantidad * dv.precio) AS IngresoTotal,
                                SUM(dv.cantidad) AS ProductosVendidos,
                                SUM(dv.cantidad * dv.precio) * 0.15 AS Ganancia
                            FROM 
                                venta v
                                INNER JOIN detalle_venta dv ON v.id = dv.Venta_id
                                INNER JOIN producto p ON dv.Producto_id = p.id
                            GROUP BY 
                                DATE_FORMAT(v.fecha, '%Y')
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_detalles_venta_para_pdf(self, id_venta):
        # Obtener detalles de una venta específica para PDF
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                p.nombre,
                                dv.cantidad,
                                dv.precio AS precio_unitario,
                                (dv.cantidad * dv.precio) AS subtotal,
                                v.total_venta
                            FROM 
                                detalle_venta dv
                                JOIN producto p ON dv.Producto_id = p.id
                                JOIN venta v ON dv.Venta_id = v.id
                            WHERE 
                                v.id = %s""", (id_venta,))
            return cursor.fetchall()
        

    def obtener_compras(self): # Devuelve IdCompra, Proveedor, Empleado, FechaCompra, Total
        # Obtener compras
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                c.id AS IdCompra, 
                                p.nombre AS Proveedor, 
                                e.nombre AS Empleado, 
                                c.fecha AS FechaCompra, 
                                c.total_compra AS Total
                            FROM 
                                proveedor p
                                INNER JOIN compra c ON p.id = c.Proveedor_id
                                INNER JOIN empleado e ON e.id = c.Empleado_id
                            WHERE
                                c.estado = 1
                            GROUP BY 
                                c.id""")
            return cursor.fetchall()

    def obtener_detalles_por_id_compra(self, id_compra): # Devuelve IdOrden, Producto, CantidadRecibida, Total
        # Obtener detalles de una compra específica
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                dc.id AS IdOrden, 
                                p.nombre AS Producto, 
                                dc.cantidad_recibida AS CantidadRecibida, 
                                dc.precio_unitario * dc.cantidad_recibida AS Total
                            FROM 
                                compra c
                                INNER JOIN detalle_compra dc ON c.id = dc.Compra_id
                                INNER JOIN producto p ON p.id = dc.Producto_id
                            WHERE 
                                c.id = %s""", (id_compra,))
            return cursor.fetchall()

    def obtener_reporte_compras_por_dia(self):
        # Obtener compras "Fecha", "CantidadProductos", "Gastos"
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE(c.fecha) AS Fecha,
                                SUM(dc.cantidad_recibida) AS CantidadProductos,
                                SUM(dc.cantidad_recibida * dc.precio_unitario) AS Gastos
                            FROM 
                                compra c
                                INNER JOIN detalle_compra dc ON c.id = dc.Compra_id
                            WHERE
                                c.estado = 1
                            GROUP BY 
                                DATE(c.fecha)
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_reporte_compras_por_mes(self):
        # Obtener compras por mes
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE_FORMAT(c.fecha, '%Y-%m') AS Fecha,
                                SUM(dc.cantidad_recibida) AS CantidadProductos,
                                SUM(dc.cantidad_recibida * dc.precio_unitario) AS Gastos
                            FROM 
                                compra c
                                INNER JOIN detalle_compra dc ON c.id = dc.Compra_id
                            WHERE
                                c.estado = 1
                            GROUP BY 
                                DATE_FORMAT(c.fecha, '%Y-%m')
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_reporte_compras_por_anio(self):
        # Obtener compras por año
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE_FORMAT(c.fecha, '%Y') AS Fecha,
                                SUM(dc.cantidad_recibida) AS CantidadProductos,
                                SUM(dc.cantidad_recibida * dc.precio_unitario) AS Gastos
                            FROM 
                                compra c
                                INNER JOIN detalle_compra dc ON c.id = dc.Compra_id
                            WHERE
                                c.estado = 1
                            GROUP BY 
                                DATE_FORMAT(c.fecha, '%Y')
                            ORDER BY 
                                Fecha DESC""")
            return cursor.fetchall()
        
    def obtener_reporte_compras_por_fecha(self, fecha_inicio, fecha_fin): # fecha, orden_id, proveedor, total, productos_totales
        with self.conexion.cursor() as cursor:
            cursor.execute("""SELECT 
                                DATE(c.fecha) AS fecha,
                                c.id AS orden_id,
                                p.nombre AS proveedor,
                                c.total_compra AS total,
                                SUM(dc.cantidad_recibida) AS productos_totales
                            FROM 
                                compra c
                                JOIN detalle_compra dc ON c.id = dc.Compra_id
                                JOIN proveedor p ON c.Proveedor_id = p.id
                            WHERE 
                                c.estado = 1 AND
                                c.fecha BETWEEN %s AND %s
                            GROUP BY 
                                c.id
                            ORDER BY 
                                c.fecha DESC""", (fecha_inicio, fecha_fin))
            return cursor.fetchall()
        
        
