{
   'name': 'Freight  Fix',
   'version': '19.0.0.0.0',
   'depends': ['bi_freight_management'],
   'summary': 'Correcciones y extensiones sobre bi_freight_management (monedas, folios, Accounting, Tracking).',
   'description': """
      Freight Fix - Extensiones a bi_freight_management
      ==================================================

      Este módulo NO modifica los archivos originales de bi_freight_management;
      todo se agrega por herencia (_inherit), para poder actualizar el módulo
      base sin perder estos cambios.

      Cambios incluidos:

      * Folio de shipments y bookings: al Duplicar un registro ya no se repite
        el mismo folio (name); se genera uno nuevo por secuencia.
      * Montos Expected/Actual Receivable y Payable: se convierten a la moneda
        de la compañía antes de sumar, en vez de mezclar distintas divisas.
      * Wizard de Factura/Bill desde Services: valida que todas las líneas
        seleccionadas usen la misma moneda antes de crear la factura, y respeta
        esa moneda en vez de forzar la moneda por defecto de Odoo.
      * Pestaña Accounting del shipment: Agrega la columna Programming Bill
      * Tracking: el campo Date pasa de Fecha a Fecha y Hora (Datetime).
      """,
   'license': 'OPL-1',
   'author': 'Grupo Sachman',
   'data': [
        'views/freight_operation_accounting_services.xml',
    ],
    'installable': True,
}