odoo.define('pos_lista_precio.ProductScreen', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PosListaPrecioProductScreen = (ProductScreen) => class extends ProductScreen {
        _onClickPay() {
            let cliente = this.currentOrder.get_client();
            if (cliente) {
                super._onClickPay(...arguments);
            } else {
                this.showPopup('ErrorPopup', {
                    title: 'Seleccionar cliente',
                    body: 'Por favor seleccionar cliente antes de pasar a la ventana de pago.',
                });
            }
        }
    };

    Registries.Component.extend(ProductScreen, PosListaPrecioProductScreen);
    return ProductScreen;

});