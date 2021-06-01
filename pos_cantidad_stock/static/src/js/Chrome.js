odoo.define('pos_cantidad_stock.Chrome', function (require) {
    "use strict";

    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');
    const models = require('point_of_sale.models');

    const PosCantidadStockChrome = (Chrome) => class extends Chrome {
        async start() {
            super.start(...arguments);
            //0 - todos , 1 - con existencia, 2 - sin existencia
            this.env.pos.set(
                'porExistencia',
                1
            );
        }
    };

    Registries.Component.extend(Chrome, PosCantidadStockChrome);
    return Chrome;

});