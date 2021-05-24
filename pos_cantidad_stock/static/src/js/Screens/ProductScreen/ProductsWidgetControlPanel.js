odoo.define('pos_cantidad_stock.ProductsWidgetControlPanel', function (require) {
    "use strict";

    const ProductsWidgetControlPanel = require('point_of_sale.ProductsWidgetControlPanel');
    const Registries = require('point_of_sale.Registries');

    const PosCantidadStockProductsWidgetControlPanel = (ProductsWidgetControlPanel) => class extends ProductsWidgetControlPanel {
        tot_existencia() {
            this.trigger('switch-por-existencia', 0);
        }
        con_existencia() {
            this.trigger('switch-por-existencia', 1);
        }
        sin_existencia() {
            this.trigger('switch-por-existencia', 2);
        }
    };

    Registries.Component.extend(ProductsWidgetControlPanel, PosCantidadStockProductsWidgetControlPanel);
    return ProductsWidgetControlPanel;

});