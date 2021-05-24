odoo.define('pos_lista_precio.PaymentScreen', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosListaPrecioPaymentScreen = (PaymentScreen) => class extends PaymentScreen {
        async selectClient() {

        }
    };

    Registries.Component.extend(PaymentScreen, PosListaPrecioPaymentScreen);
    return PaymentScreen;

});