# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
      - Se modifico el módelo de 'report.stock.quantity' en donde se agregó el campo de
        categoría de producto 'x_product_category' lo que nos ayudara en obtener una mejor
        visibilidad en el inventario previsto.
      - Se agregaron campos de categoria de producto en los modelos 'stock.move' y 'stock.quant'
        para poder realizar la union de aquellas tablas en el query.
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 26/04/2021
    *************************************************************************/
'''

from odoo import models, fields, api, tools

class report_stock_quantity_custom(models.Model):
    _inherit = 'report.stock.quantity'

    x_product_category = fields.Many2one('product.category', string="Categoría de producto",readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_quantity')
        query = """
    CREATE or REPLACE VIEW report_stock_quantity AS (
    WITH forecast_qty AS (
        SELECT
            m.id,
            m.product_id,
            CASE
                WHEN (whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit' THEN 'out'
                WHEN (whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit' THEN 'in'
            END AS state,
            m.date::date AS date,
            CASE
                WHEN (whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit' THEN -product_qty
                WHEN (whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit' THEN product_qty
            END AS product_qty,
            m.company_id,
            CASE
                WHEN (whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit' THEN whs.id
                WHEN (whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit' THEN whd.id
            END AS warehouse_id,
            m.x_product_category 
        FROM
            stock_move m
        LEFT JOIN stock_location ls on (ls.id=m.location_id)
        LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
        LEFT JOIN stock_warehouse whs ON ls.parent_path like concat('%/', whs.view_location_id, '/%')
        LEFT JOIN stock_warehouse whd ON ld.parent_path like concat('%/', whd.view_location_id, '/%')
        LEFT JOIN product_product pp on pp.id=m.product_id
        LEFT JOIN product_template pt on pt.id=pp.product_tmpl_id
        WHERE
            pt.type = 'product' AND
            product_qty != 0 AND
            (whs.id IS NOT NULL OR whd.id IS NOT NULL) AND
            (whs.id IS NULL OR whd.id IS NULL OR whs.id != whd.id) AND
            m.state NOT IN ('cancel', 'draft', 'done')
        UNION ALL
        SELECT
            -q.id as id,
            q.product_id,
            'forecast' as state,
            date.*::date,
            q.quantity as product_qty,
            q.company_id,
            wh.id as warehouse_id,
            q.x_product_category
        FROM
            GENERATE_SERIES((now() at time zone 'utc')::date - interval '3month',
            (now() at time zone 'utc')::date + interval '3 month', '1 day'::interval) date,
            stock_quant q
        LEFT JOIN stock_location l on (l.id=q.location_id)
        LEFT JOIN stock_warehouse wh ON l.parent_path like concat('%/', wh.view_location_id, '/%')
        WHERE
            (l.usage = 'internal' AND wh.id IS NOT NULL) OR
            l.usage = 'transit'
        UNION ALL
        SELECT
            m.id,
            m.product_id,
            'forecast' as state,
            GENERATE_SERIES(
            CASE
                WHEN m.state = 'done' THEN (now() at time zone 'utc')::date - interval '3month'
                ELSE m.date::date
            END,
            CASE
                WHEN m.state != 'done' THEN (now() at time zone 'utc')::date + interval '3 month'
                ELSE m.date::date - interval '1 day'
            END, '1 day'::interval)::date date,
            CASE
                WHEN ((whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit') AND m.state = 'done' THEN product_qty
                WHEN ((whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit') AND m.state = 'done' THEN -product_qty
                WHEN (whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit' THEN -product_qty
                WHEN (whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit' THEN product_qty
            END AS product_qty,
            m.company_id,
            CASE
                WHEN (whs.id IS NOT NULL AND whd.id IS NULL) OR ls.usage = 'transit' THEN whs.id
                WHEN (whs.id IS NULL AND whd.id IS NOT NULL) OR ld.usage = 'transit' THEN whd.id
            END AS warehouse_id,
            m.x_product_category AS x_product_category
        FROM
            stock_move m
        LEFT JOIN stock_location ls on (ls.id=m.location_id)
        LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
        LEFT JOIN stock_warehouse whs ON ls.parent_path like concat('%/', whs.view_location_id, '/%')
        LEFT JOIN stock_warehouse whd ON ld.parent_path like concat('%/', whd.view_location_id, '/%')
        LEFT JOIN product_product pp on pp.id=m.product_id
        LEFT JOIN product_template pt on pt.id=pp.product_tmpl_id
        WHERE
            pt.type = 'product' AND
            product_qty != 0 AND
            (whs.id IS NOT NULL OR whd.id IS NOT NULL) AND
            (whs.id IS NULL or whd.id IS NULL OR whs.id != whd.id) AND
            m.state NOT IN ('cancel', 'draft')
    ) -- /forecast_qty
    SELECT
        MIN(id) as id,
        product_id,
        state,
        date,
        sum(product_qty) as product_qty,
        company_id,
        warehouse_id,
        x_product_category
    FROM forecast_qty
    GROUP BY product_id, state, date, company_id, warehouse_id, x_product_category
    );
    """
        self.env.cr.execute(query)