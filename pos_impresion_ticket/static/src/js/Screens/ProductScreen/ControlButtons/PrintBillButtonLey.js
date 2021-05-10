console.log('PrintBillButtonLey');
odoo.define('pos_impresion_ticket.PrintBillButtonLey', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class PrintBillButtonLey extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const order = this.env.pos.get_order();
            if (order.get_orderlines().length > 0) {
                console.log('this =>', this)
                await this.showTempScreen('ImprimirTicketScreen');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nada para imprimir'),
                    body: this.env._t('No existen líneas de producto en esta orden de venta.'),
                });
            }
        }
    }
    PrintBillButtonLey.template = 'PrintBillButtonLey';

    ProductScreen.addControlButton({
        component: PrintBillButtonLey,
        condition: function() {
            return this.env.pos.config.imprimir_ticket;
        },
    });

    Registries.Component.add(PrintBillButtonLey);

    return PrintBillButtonLey;
});
