from odoo import models, fields

class ProductPfFamily(models.Model):
    _name = 'product.pf.family'
    _description = 'Familia de productos'

    name = fields.Char('Nombre')
    active = fields.Boolean(default=True)


class ProductPfFormat(models.Model):
    _name = 'product.pf.format'
    _description = 'Formato'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)

class ProductPfTech(models.Model):
    _name = 'product.pf.tech'
    _description = 'Tecnología'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)

class ProductPfPower(models.Model):
    _name = 'product.pf.power'
    _description = 'Potencia'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)

class ProductPfCapacity(models.Model):
    _name = 'product.pf.capacity'
    _description = 'Capacidad'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)

class ProductPfBrand(models.Model):
    _name = 'product.pf.brand'
    _description = 'Marca'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)

class ProductPfColor(models.Model):
    _name = 'product.pf.color'
    _description = 'Color'

    pf_family_id = fields.Many2one(comodel_name="product.pf.family",string="Familia",required=True)
    name = fields.Char('Nombre')    
    active = fields.Boolean(default=True)