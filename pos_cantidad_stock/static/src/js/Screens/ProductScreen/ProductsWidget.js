odoo.define('pos_cantidad_stock.ProductsWidget', function (require) {
    "use strict";

    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');

    const PosCantidadStockProductsWidget = (ProductsWidget) => class extends ProductsWidget {
        constructor() {
            super(...arguments);
            useListener('switch-por-existencia', this._switchPorExistencia);
        }
        mounted() {
            super.mounted(...arguments);
            this.env.pos.on('change:porExistencia', this.render, this);
        }
        willUnmount() {
            super.willUnmount(...arguments);
            this.env.pos.off('change:porExistencia', null, this);
        }
        get porExistencia() {
            return this.env.pos.get('porExistencia');
        }
        _switchPorExistencia(value) {
            return this.env.pos.set('porExistencia', value.detail);
        }
        get productsToDisplay() {
            if (this.searchWord !== '') {
                return this.env.pos.db.search_product_in_category(
                    this.selectedCategoryId,
                    this.searchWord,
                    this.porExistencia
                );
            }
            else {
                return this.env.pos.db.get_product_by_category(this.selectedCategoryId, this.porExistencia);
            }
        }
    };

    Registries.Component.extend(ProductsWidget, PosCantidadStockProductsWidget);
    return ProductsWidget;

});