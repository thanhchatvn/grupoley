# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
    * Se creo un módelo transitorio llamado 'import.sale.order' el cual nos ayuda a importar
      ordenes de compra realizadas por Casa Ley y crear ordenes de venta dentro de Odoo
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 16/04/2021
    *************************************************************************/
'''

import base64
import csv
import io
import os
import tempfile
from odoo.exceptions import UserError
from dateutil import parser
from odoo import fields, models, api, _

class ImportChartAccount(models.TransientModel):
    _name = "import.sale.order"
    _description = "Módelo que nos permite importar un pedido de orden de compra de Casa Ley"

    file_data = fields.Binary(string="Select txt File", required=True)
    file_name = fields.Char(string='File Name')

    # Acción que se realiza al presionar el boton de "Importar"
    def imoport_file(self):
        # Validamos la extensión del archivo
        if not self.txt_validator(self.file_name):
            raise UserError(_("El archivo debe ser de extension .txt"))

        # Creación de los archivos temporales
        file_path_txt = tempfile.gettempdir() + '/sale_order.txt'
        file_path_csv = tempfile.gettempdir() + '/sale_order.csv'

        # Escritura del archivo temporal 'sale_order.txt'
        file = open(file_path_txt, 'w')

        # Llaves con las que se identificaran los valores de cada columna
        keys = ['estado', 'ciudad', 'tienda', 'nombre_tda', 'subfamilia', 'nombre_subfamilia', 'grupo_categoria',
                'categoria', 'desc_categoria', 'folio_pedido', 'proveedor', 'desc_proveedor', 'articulo',
                'codigo_upc', 'desc_articulo', 'contenido', 'factor_calculo', 'cantidad_pedida']

        # Decodificamos nuestro archivo txt
        txt_data = base64.b64decode(self.file_data)
        # Lo formateamos a codificación UTF-8
        data_file = io.StringIO(txt_data.decode("utf-8"))

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

        # Leemos nuestro archivo csv y creamos un diccionario para identificar sus valores
        csv_file = open(file_path_csv, 'r')
        file_reader = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        file_reader.extend(csv_reader)
        archive = csv.DictReader(open(file_path_csv))
        archive_lines = []

        for line in archive:
            archive_lines.append(line)

        # Creamos nuestros objetos para tener acceso a sus campos
        customer_obj = self.env['res.partner']
        product_obj = self.env['product.product']

        # Etapa de validación de existencia o duplicidad
        self.valid_customer(archive_lines, customer_obj)
        self.valid_product_code(archive_lines, product_obj)
        csv_file.close()

        # Se crea un solo pedido de venta dependiendo del folio de pedido de compra
        sale_orders = []
        for i in range(len(file_reader)):
            field = list(map(str, file_reader[i]))
            values = dict(zip(keys, field))
            sale_order = str(values.get('folio_pedido'))

            if values:
                if i == 0:
                    continue
                elif sale_order not in sale_orders:
                    values.update({
                        'tienda': field[2],
                        'folio_pedido': field[9],
                        'fecha_pedido': field[18],
                    })
                    self.create_chart_accounts(values, archive_lines)
                else:
                    pass

            if sale_order != None:
                sale_orders.append(sale_order)

    # Creación de las ordenes de venta
    def create_chart_accounts(self, values, archive_lines):
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        product_obj = self.env['product.product']
        tienda = values.get('tienda')
        company = self.env.company
        customer = self.env['res.partner'].search(
            [('x_center', '=', tienda), ('company_id', '=', company.id), ('parent_id.name', 'ilike', 'ley')], limit=1)
        customer_id = customer.id
        if customer.user_id:
            comercial = customer.user_id.id
            if customer.user_id.property_warehouse_id:
                warehouse_id = customer.user_id.property_warehouse_id.id
            else:
                error = ("El comercial [{}] no tiene asignado un almacen:").format(customer.user_id.name)
                raise UserError(error)
        else:
            error = ("El cliente [{}] no tiene asignado un comercial").format(customer.name)
            raise UserError(error)
        if customer.property_payment_term_id:
            payment_term = customer.property_payment_term_id.id
        else:
            payment_term = None

        folio_pedido = values.get('folio_pedido')
        fecha_pedido = parser.parse(values.get('fecha_pedido'))

        data = {
            'partner_id': customer_id,
            'user_id': comercial,
            'payment_term_id': payment_term,
            'warehouse_id': warehouse_id,
            'client_order_ref': folio_pedido,
            'x_order_reference': folio_pedido,
            'x_order_reference_date': fecha_pedido,
        }
        sale_order_id = sale_order_obj.create(data)

        for line in archive_lines:
            folio = line.get('FOLIO PEDIDO')
            # Verificamos si existe un folio de pedio de compra en el archivo
            if folio == folio_pedido:
                barcode = str(line.get('ARTICULO', "")).strip()
                product_id = product_obj.search([('x_product_supplierinfo.product_code', 'like', barcode)], limit=1)
                quantity = line.get('CANTIDAD PEDIDA', 0)
                route = customer.x_studio_ruta.id

                # Si existe una orden de venta y producto que coincidan se llenara nuestro linea de pedido
                if sale_order_id and product_id:
                    vals = {
                        'order_id': sale_order_id.id,
                        'product_id': product_id.id,
                        'product_uom_qty': float(quantity),
                        'name': product_id.display_name,
                        'route_id': route,
                    }
                    sale_order_line_obj.create(vals)

            else:
                pass
        sale_order_id.update_prices()
        return {'type': 'ir.actions.act_window_close'}

    # Validación de existencia y duplicidad de productos en el sistema
    @api.model
    def valid_product_code(self, archive_lines, product_obj):
        counter = 0
        for line in archive_lines:
            counter += 1
            code = str(line.get('ARTICULO', "")).strip()
            product_name = str(line.get('DESC ARTICULO', "")).strip()
            product_id = product_obj.search([('x_product_supplierinfo.product_code', 'like', code)])
            product_content = str(line.get('CONTENIDO', "")).strip()

            # Si se encuentran más productos con el mismo código
            if len(product_id) > 1:
                duplicated_product = []
                for product in product_id:
                    duplicated_product.append(product.name)
                error = ("Linea de pedido: {}\n\n"
                         "Existen productos con el mismo código [{}] en el sistema\n\n"
                         "Productos con código duplicado: {}.").format(counter, code, duplicated_product)
                raise UserError(error)

            # Si no se encuentran productos que coincidan con el código
            if not product_id:
                error = ("Linea de pedido: {}\n\n"
                         "No existe ningun producto con el código [{}] en el sistema.\n\n"
                         "Nombre del producto [{} {}]").format(counter, code, product_name, product_content)
                raise UserError(error)

    # Validación de existencia y duplicidad de clientes en el sistema
    @api.model
    def valid_customer(self, archive_lines, customer_obj):
        counter = 0
        for line in archive_lines:
            counter += 1
            tienda = str(line.get('TIENDA', "")).strip()
            company = self.env.company
            partner_id = customer_obj.search(
                [('x_center', '=', tienda), ('company_id', '=', company.id), ('parent_id.name', 'ilike', 'ley')])

            # Si se encuentran más clientes con la misma tienda
            if len(partner_id) > 1:
                error = ("Linea de pedido: {}\n\n"
                         "Los clientes [{}] [{}] tienen la misma tienda.").format(counter, partner_id[0].name,
                                                                                  partner_id[1].name)
                raise UserError(error)

            # Si no se encuentran clientes que coincidan con su tienda
            if not partner_id:
                error = ("Linea de pedido: {}\n\n"
                         "El cliente no se encuentra en el sistema o su tienda {} no está establecida.").format(counter,
                                                                                                                tienda)
                raise UserError(error)

    # Validación de extensión del archivo
    @api.model
    def txt_validator(self, file_name):
        name, extension = os.path.splitext(file_name)
        return True if extension == '.txt' else False
