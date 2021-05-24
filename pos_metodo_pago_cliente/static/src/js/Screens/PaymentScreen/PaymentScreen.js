console.log('pos_metodo_pago_cliente.PaymentScreen')
odoo.define('pos_addenda_custom.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const MetodoPagoClientePaymentScreen = (PaymentScreen) => class extends PaymentScreen {

        _updateSelectedPaymentline() {
            if (this.paymentLines.every((line) => line.paid)) {
                let property_payment_term_id = this.currentOrder.get_client().property_payment_term_id
                let x_l10n_mx_edi_payment_method_id = this.currentOrder.get_client().x_l10n_mx_edi_payment_method_id
                let payment_method_temp = JSON.parse(JSON.stringify(this.env.pos.payment_methods))[0];
                if (property_payment_term_id[1] == 'Contado'){
                    payment_method_temp = this.env.pos.payment_methods.find(e => e.name == "Efectivo")
                } else {
                    if (x_l10n_mx_edi_payment_method_id[1] == 'Transferencia electrónica de fondos'){
                        payment_method_temp = JSON.parse(JSON.stringify(this.env.pos.payment_methods.find(e => e.name == "Transferencia electrónica")))
                    } else {
                        payment_method_temp = this.env.pos.payment_methods.find(e => e.name == "Crédito")
                    }
                }
                this.currentOrder.add_paymentline(payment_method_temp);
            }
            if (!this.selectedPaymentLine) return;
            if (
                this.payment_interface &&
                !['pending', 'retry'].includes(this.selectedPaymentLine.get_payment_status())
            ) {
                return;
            }
            if (NumberBuffer.get() === null) {
                this.deletePaymentLine({ detail: { cid: this.selectedPaymentLine.cid } });
            } else {
                this.selectedPaymentLine.set_amount(NumberBuffer.getFloat());
            }
        }

    };

    Registries.Component.extend(PaymentScreen, MetodoPagoClientePaymentScreen);
    return PaymentScreen;

});