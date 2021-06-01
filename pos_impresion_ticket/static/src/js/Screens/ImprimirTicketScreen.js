odoo.define('pos_impresion_ticket.ImprimirTicketScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const ImprimirTicketScreen = (ReceiptScreen) => {
        class ImprimirTicketScreen extends ReceiptScreen {
            confirm() {
                this.props.resolve({ confirmed: true, payload: null });
                this.trigger('close-temp-screen');
            }
        }
        ImprimirTicketScreen.template = 'ImprimirTicketScreen';
        return ImprimirTicketScreen;
    };

    Registries.Component.addByExtending(ImprimirTicketScreen, ReceiptScreen);

    return ImprimirTicketScreen;
});
