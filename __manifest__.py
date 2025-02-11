{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Alquiler de productos de una empresa.',
    'description': """
    Módulo para gestionar el alquiler de productos de una empresa.
    Permite asignar préstamos incluyendo: un cliente, un producto, 
    una fecha de inicio, una fecha final, un estado y una observación.
    """,
    'author': 'Pablo Muiño',
    'depends': ['base', 'sale', 'contacts'], # Requiere módulos base, ventas y contactos
    'data': [
        'views/alquiler_productos_views.xml',
        'views/alquiler_productos_menu.xml',
        'security/ir.model.access.csv',
    ],
    'icon': '/alquiler_productos/static/description/icon56.png',
    'installable': True,
    'application': True,
}