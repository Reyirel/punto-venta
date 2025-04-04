# Sistema de Punto de Venta

Este proyecto es un sistema de punto de venta desarrollado en Python utilizando Tkinter para la interfaz gráfica y SQLite como base de datos. El sistema cuenta con módulos para la administración, ventas, gestión de clientes, productos, reportes y control de usuarios.

## Características

- **Interfaz gráfica**: Panel para administradores y vendedores.
- **Gestión de usuarios**: Ingreso, roles (admin y vendedor).
- **Control de productos**: Agregar, modificar, eliminar y búsqueda de productos.
- **Gestión de clientes**: Crear, editar y eliminar clientes con saldo.
- **Ventas**: Registro de ventas, emisión de reportes y exportación a Excel.
- **Reportes de ventas**: Filtrado por fecha y actualización automática.

## Estructura del Proyecto

- **README.md**: Este archivo.
- **.vscode/**: Configuraciones de Visual Studio Code.
- **src/**: Contiene el código fuente principal:
  - [main.py](l:/luisn/Documents/vinateria/src/main.py): Punto de entrada y creación de tablas de la base de datos.
  - [login.py](l:/luisn/Documents/vinateria/src/login.py): Lógica de autenticación.
  - [admin_panel.py](l:/luisn/Documents/vinateria/src/admin_panel.py): Interfaz y módulos del panel de administración.
  - [vendedor_panel.py](l:/luisn/Documents/vinateria/src/vendedor_panel.py): Interfaz y módulos para el panel de vendedor.
  - **models/**
    - [database.py](l:/luisn/Documents/vinateria/src/models/database.py): Conexión y creación de tablas en la base de datos.
  - **data/**
    - Archivo de base de datos: `punto_venta.db`.

## Instalación

1. Asegúrate de tener Python instalado (recomendado Python 3.10 o superior).
2. Instala las dependencias necesarias:
   ```sh
   pip install pillow pandas
   ```
3. (Opcional) Configura tu entorno de desarrollo con Visual Studio Code usando la configuración de la carpeta [.vscode/settings.json](l:/luisn/Documents/vinateria/.vscode/settings.json).

## Uso

1. Ejecuta el proyecto desde la carpeta raíz:
   ```sh
   python src/main.py
   ```
2. En la pantalla de login, utiliza uno de los siguientes usuarios predeterminados:
   - **Administrador**: `admin` / `admin123`
   - **Vendedor**: `vendedor` / `vendedor123`

3. Una vez autenticado, se mostrará el panel correspondiente según el rol.

## Funcionalidades Adicionales

- **Exportar reportes**: Desde el panel de reportes se puede exportar la información de ventas a archivos Excel.
- **Actualización automática**: Las ventas se refrescan automáticamente cada 5 segundos.
- **Gestión de stock y clientes**: Actualización de inventario y saldo de clientes durante las ventas.

## Licencia

Este proyecto es de código abierto y se distribuye bajo la licencia MIT.
