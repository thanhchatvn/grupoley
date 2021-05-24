odoo.define('pos_cantidad_stock.ProductItem', function (require) {
    "use strict";

    const ProductItem = require('point_of_sale.ProductItem');
    const Registries = require('point_of_sale.Registries');

    var models = require('point_of_sale.models');
//    models.load_fields('product.product', 'qty_available');

    const PosCantidadStockProductItem = (ProductItem) => class extends ProductItem {
        get cantidad() {
            return this.props.product.qty_available;
        }
        get rounded_qty() {
            return this.props.product.rounded_qty();
        }
    };

    Registries.Component.extend(ProductItem, PosCantidadStockProductItem);
    return ProductItem;

});