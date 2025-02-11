from odoo import models, fields, api
from datetime import timedelta

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _order = 'number asc'

    number = fields.Integer(string='Número de préstamo', required=True, copy=False, default=0)
    customer_id = fields.Many2one('res.partner', string='Cliente', required=True)
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    rent_day = fields.Date(string='Fecha de Alquiler', required=True)
    warranty_date = fields.Date(string='Fecha de Vencimiento', compute='_compite_warranty_date', store=True)
    status = fields.Selection([
        ('rented', 'En alquiler'),
        ('delivered', 'Entregado'),
        ('not_delivered', 'No entregado')
    ], string='Estado', compute='_compute_status', store=True)
    observations = fields.Text(string='Observaciones')

    @api.model
    def create(self, vals):
        # Lógica para calcular el número de préstamo automáticamente
        last_number = self.search([], order="number desc", limit=1).number
        vals['number'] = last_number + 1 if last_number else 1 # Si no hay registros, empieza con 1
        return super(AlquilerProducto, self).create(vals)
    
    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            # Verificar si el producto tiene stock disponible
            if self.product_id.qty_available <= 0:
                return {
                    'warning': {
                        'title': 'Producto no disponible',
                        'message': 'El producto seleccionado no está disponible en inventario.'
                    }
                }
    
    @api.depends('rent_date')
    def _compute_warranty_date(self):
        for record in self:
            if record.rent_day:
                # Sumamos 30 días directamente a la fecha de alquiler
                record.warranty_date = record.rent_day + timedelta(days=30)
            else:
                # Si no hay fecha de alquiler, el campo se deja vacío
                record.warranty_date = False

    @api.depends('warranty_date')
    def _compute_status(self):
        for record in self:
            if record.warranty_date and record.warranty_date < fields.Date.today():
                record.status = 'not_delivered'
            else:
                record.status = 'rented'

    @api.model
    def _update_rental_status(self):
        rentals = self.search([('status', '=', 'rented'), ('warranty_date', '<', fields.Date.today())])
        for rental in rentals:
            rental.status = 'not_delivered'
    
    def write(self, vals):
        # Control de acceso (solo el grupo de ventas puede editar los préstamos)
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise UserError('No tienes permisos para modificar este registro.')
        return super(AlquilerProducto, self).write(vals)

    def unlink(self):
        # Control de permisos de acceso a la vista (solo los de ventas pueden editar)
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise UserError('No tienes permisos para eliminar este registro.')
        return super(AlquilerProducto, self).unlink()