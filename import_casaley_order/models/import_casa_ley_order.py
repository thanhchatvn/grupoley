# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil import parser
import os
import base64
import io
import tempfile
import csv

class CasaLeyImport(models.Model):
    _name = 'import.ley.order'
    _description = 'Interfaz de pedidos de casa ley'
    _rec_name = 'id'

    zone = fields.Many2one('zone.pam', string='Territorio', store=True)
    route = fields.Many2one('route.pam',string='Ruta', store=True)
    file_data = fields.Binary(string='Archivo', required=True)
    file_name = fields.Char(string='Nombre')
    sale_order_ids = fields.One2many('sale.orders.casa.ley', 'import_id', string='Pedidos',
                                     store=True)
    initial_date = fields.Date(string='Fecha inicial', store=True, required=True)
    end_date = fields.Date(string='Fecha final', store=True, required=True)

    def validate(self):
        global fecha_pedido
        self.sale_order_ids = [((5,0,0))]

        # Validamos el archivo txt
        if not self.txt_validator(self.file_name):
            raise UserError(_("El archivo debe ser de extension .txt"))

        # Creación de los archivos temporales
        file_path_txt = tempfile.gettempdir() + '/sale_order.txt'
        file_path_csv = tempfile.gettempdir() + '/sale_order.csv'

        # Decodificamos nuestro archivo txt
        txt_data = base64.b64decode(self.file_data)
        # Lo formateamos a codificación UTF-8
        data_file = io.StringIO(txt_data.decode("utf-8"))

        # Escritura del archivo temporal 'sale_order.txt'
        file = open(file_path_txt, 'w')

        # Validamos el formato de nuestro archivo de texto y creamos nuestra lista de valores
        try:
            for lines in data_file:
                estado = lines[0:4]
                ciudad = lines[4:8]
                tienda = lines[8:12]
                nombre_tda = lines[12:42]
                subfamilia = lines[42:45]
                nombre_subfamilia = lines[45:75]
                grupo_categoria = lines[75:78]
                categoria = lines[78:80]
                desc_categoria = lines[80:130]
                folio_pedido = lines[130:136]
                proveedor = lines[136:141]
                desc_proveedor = lines[141:191]
                articulo = lines[191:199]
                codigo_upc = lines[199:212]
                desc_articulo = lines[212:242]
                contenido = lines[242:255]
                factor_calculo = lines[255:257]
                cantidad_pedida = lines[257:267]

                if lines[284]:
                    if lines[284] == 'M':
                        fecha_pedido = lines[267:285]
                    else:
                        fecha_pedido = lines[267:286]
                line = (estado + ',' + ciudad + ',' + tienda + ',' + nombre_tda + ',' +
                        subfamilia + ',' + nombre_subfamilia + ',' + grupo_categoria + ',' +
                        categoria + ',' + desc_categoria + ',' + folio_pedido + ',' +
                        proveedor + ',' + desc_proveedor + ',' + articulo + ',' +
                        codigo_upc + ',' + desc_articulo + ',' +
                        contenido + ',' + factor_calculo + ',' + cantidad_pedida + ',' +
                        fecha_pedido + '\n')
                file.write(line)
        except:
            raise UserError(_("El archivo no tiene el formato requerido"))
        file.close()

        # Leemos nuestro archivo txt ya formateado para su conversion a csv
        with open(file_path_txt, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            # Creamos nuestro archivo temporal csv 'sale_order.csv'
            with open(file_path_csv, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('ESTADO', 'CIUDAD', 'TIENDA', 'NOMBRE TDA', 'SUBFAMILIA', 'NOMBRE SUBFAMILIA',
                                 'GRUPO CATEGORIA', 'CATEGORIA', 'DESC CATEGORIA', 'FOLIO PEDIDO',
                                 'PROVEEDOR', 'DESC PROVEEDOR', 'ARTICULO', 'CODIGO UPC', 'DESC ARTICULO',
                                 'CONTENIDO', 'FACTOR CALCULO', 'CANTIDAD PEDIDA', 'FECHA PEDIDO'))
                writer.writerows(lines)
        archive_lines = []
        archive = csv.DictReader(open(file_path_csv))
        for i in archive:
            archive_lines.append(i)

        sale_orders = []
        counter = 0

        for rec in archive_lines:
            counter += 1
            sale_order = rec.get('FOLIO PEDIDO')
            if sale_order not in sale_orders:

                sale_orders.append(sale_order)
                store = str(rec.get('TIENDA')).strip()
                date_order = rec.get('FECHA PEDIDO')
                partner_id = self.valid_customer(store, counter)
                self.load_orders(sale_order, partner_id, date_order, archive_lines, counter)
            else:
                pass

    @api.model
    # Carga de las ordenes de venta
    def load_orders(self, sale_order, partner_id, date_order, archive, counter):
        if partner_id.user_id:
            comercial = partner_id.user_id.id
            if partner_id.user_id.property_warehouse_id:
                warehouse_id = partner_id.user_id.property_warehouse_id.id
            else:
                error = ("El comercial [{}] no tiene asignado un almacen:").format(str(partner_id.user_id.name).strip())
                raise UserError(error)
        else:
            error = ("El cliente [{}] no tiene asignado un comercial").format(str(partner_id.name).strip())
            raise UserError(error)

        if partner_id.property_payment_term_id:
            payment_term = partner_id.property_payment_term_id.id
        else:
            payment_term = None

        date_order = parser.parse(date_order)

        data = {
            'name': sale_order,
            'partner_id': partner_id.id,
            'user_id': comercial,
            'payment_term_id': payment_term,
            'warehouse_id': warehouse_id,
            'date_order': date_order
        }
        sale_orders_casa_ley_obj = self.env['sale.orders.casa.ley'].create(data)

        # FILTROS
        self.filter_orders(sale_order, sale_orders_casa_ley_obj)

        # CARGA DE PRODUCTOS EN LAS ORDENES
        for line in archive:
            folio = line.get('FOLIO PEDIDO')
            if folio == sale_order:
                barcode = str(line.get('ARTICULO')).strip()
                product_code = str(line.get('ARTICULO')).strip()
                product_name = str(line.get('DESC ARTICULO')).strip()
                product_content = str(line.get('CONTENIDO')).strip()
                order_qty = line.get('CANTIDAD PEDIDA', 0)
                route = partner_id.x_studio_ruta.id
                product_id = self.valid_product_code(product_code, product_name, product_content, counter)
                if sale_orders_casa_ley_obj and product_id:
                    vals = {
                        'sale_order_id': sale_orders_casa_ley_obj.id,
                        'product_id': product_id.id,
                        'qty_uom': float(order_qty),
                        'name': product_id.display_name,
                        'route_id': route,
                    }
                    for sale in self.sale_order_ids:
                        if folio ==  sale.name:
                            sale.order_lines = [((0, 0, vals))]

    # Validación de existencia y duplicidad de clientes en el sistema
    @api.model
    def valid_customer(self, store, counter):
        customer_obj = self.env['res.partner']
        company = self.env.company
        partner_id = customer_obj.search(
            [
                ('x_center', '=', store),
                ('company_id', '=', company.id),
                ('parent_id.name', 'ilike', 'ley')
            ], limit=1)
        if partner_id:
            return partner_id
        # Si no se encuentran clientes que coincidan con su tienda
        else:
            error = ("Linea de pedido: {}\n\n"
                     "El cliente no se encuentra en el sistema o su tienda {}"
                     " no está establecida.").format(counter, store)
            raise UserError(error)

    #VALIDAMOS QUE EL PRODUCTO TENGA ASIGNADO EL CÓDIGO DE LEY
    @api.model
    def valid_product_code(self, code, product_name, product_content, counter):
        product_obj = self.env['product.product']
        product_id = product_obj.search([('x_product_supplierinfo.product_code', 'like', code)], limit=1)

        if product_id:
            return product_id
        # Si no se encuentran productos que coincidan con el código
        else:
            error = ("Linea de pedido: {}\n\n"
                     "No existe ningun producto con el código [{}] en el sistema.\n\n"
                     "Nombre del producto [{} {}]").format(counter, code, product_name, product_content)
            raise UserError(error)

    #VALIDCACIÓN DE EXTENSIÓN DEL ARCHIVO
    @api.model
    def txt_validator(self, file_name):
        name, extension = os.path.splitext(file_name)
        return True if extension == '.txt' else False

    @api.model
    #LLENADO DE ORDENES EN INTERFAZ PRINCIPAL CON FILTROS
    def filter_orders(self, sale_order, sale_orders_casa_ley_obj):
        if self.route and not self.zone:
            sale_order_filter_obj = self.env['sale.orders.casa.ley'].search([
                '&', '&','&','&',
                ('name', '=', sale_order),
                ('id', '=', sale_orders_casa_ley_obj.id),
                ('partner_id.x_route', '=', self.route.id),
                ('date_order','>=',self.initial_date),
                ('date_order', '<=', self.end_date)
            ])
            lines = []
            for sale in sale_order_filter_obj:
                values = {
                    'name': sale.name,
                    'partner_id': sale.partner_id.id,
                    'user_id': sale.user_id.id,
                    'payment_term_id': sale.payment_term_id.id,
                    'warehouse_id': sale.warehouse_id.id,
                    'date_order': sale.date_order
                }
                lines.append(((0, 0, values)))
            self.sale_order_ids = lines

        elif self.zone and not self.route:
            sale_order_filter_obj = self.env['sale.orders.casa.ley'].search([
                '&', '&','&','&',
                ('name', '=', sale_order),
                ('id', '=', sale_orders_casa_ley_obj.id),
                ('partner_id.x_zone', '=', self.zone.id),
                ('date_order', '>=', self.initial_date),
                ('date_order', '<=', self.end_date)
            ])
            lines = []
            for sale in sale_order_filter_obj:
                values = {
                    'name': sale.name,
                    'partner_id': sale.partner_id.id,
                    'user_id': sale.user_id.id,
                    'payment_term_id': sale.payment_term_id.id,
                    'warehouse_id': sale.warehouse_id.id,
                    'date_order': sale.date_order
                }
                lines.append(((0, 0, values)))
            self.sale_order_ids = lines
        elif self.route and self.zone:
            sale_order_filter_obj = self.env['sale.orders.casa.ley'].search([
                '&', '&', '&','&','&',
                ('name', '=', sale_order),
                ('id', '=', sale_orders_casa_ley_obj.id),
                ('partner_id.x_zone', '=', self.zone.id),
                ('partner_id.x_route', '=', self.route.id),
                ('date_order', '>=', self.initial_date),
                ('date_order', '<=', self.end_date)
            ])
            lines = []
            for sale in sale_order_filter_obj:
                values = {
                    'name': sale.name,
                    'partner_id': sale.partner_id.id,
                    'user_id': sale.user_id.id,
                    'payment_term_id': sale.payment_term_id.id,
                    'warehouse_id': sale.warehouse_id.id,
                    'date_order': sale.date_order
                }
                lines.append(((0, 0, values)))
            self.sale_order_ids = lines
        else:
            sale_order_filter_obj = self.env['sale.orders.casa.ley'].search([
                '&','&','&',
                ('id', '=', sale_orders_casa_ley_obj.id),
                ('name', '=', sale_order),
                ('date_order', '>=', self.initial_date),
                ('date_order', '<=', self.end_date)
            ])
            lines = []
            for sale in sale_order_filter_obj:
                values = {
                    'name': sale.name,
                    'partner_id': sale.partner_id.id,
                    'user_id': sale.user_id.id,
                    'payment_term_id': sale.payment_term_id.id,
                    'warehouse_id': sale.warehouse_id.id,
                    'date_order': sale.date_order
                }
                lines.append((0, 0, values))
            self.sale_order_ids = lines

    #CREAMOS LOS PRESUPUESTOS DE VENTA
    @api.model
    def create_orders(self):
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        validity_date = datetime.now() + timedelta(days=1)

        for rec in self.sale_order_ids:
            data = {
                'partner_id': rec.partner_id.id,
                'user_id': rec.user_id.id,
                'payment_term_id': rec.payment_term_id.id,
                'warehouse_id': rec.warehouse_id.id,
                'client_order_ref': rec.name,
                'x_order_reference': rec.name,
                'x_order_reference_date': rec.date_order,
                'validity_date': validity_date
            }
            sale_order = sale_order_obj.create(data)

            for line in rec.order_lines:
                data = {
                    'order_id': sale_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': float(line.qty_uom),
                    'name': line.product_id.display_name,
                    'route_id': line.route_id.id,
                }
                sale_order_line_obj.create(data)
            sale_order.update_prices()

