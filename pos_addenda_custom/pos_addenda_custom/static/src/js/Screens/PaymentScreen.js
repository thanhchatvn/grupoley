odoo.define('pos_addenda_custom.LeyCustomPaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const LeyCustomPaymentScreen = (PaymentScreen) => class extends PaymentScreen {

        async addAdenda() {
            console.log('this del LeyCustomPaymentScreen =>', this)

            let inputValue1 = this.currentOrder.inputValue1;
            let inputValue2 = this.currentOrder.inputValue2;
            let inputValue3 = this.currentOrder.inputValue3;
            let inputValue4 = this.currentOrder.inputValue4;

            const { confirmed, payload } = await this.showPopup('AdendaPopup', {
                title: 'Detalles de la Addenda',
                startingValue1: inputValue1 ? inputValue1 : "",
                startingValue2: inputValue2 ? inputValue2 : "",
                startingValue3: inputValue3 ? inputValue3 : "",
                startingValue4: inputValue4 ? inputValue4 : "",
            });

            if (confirmed) {
                this.currentOrder.set_adenda(payload);
            }
        }

        async _isOrderValid(isForceValidate) {
            if (this.currentOrder.get_orderlines().length === 0) {
                this.showPopup('ErrorPopup', {
                    title: 'Pedido vacío',
                    body: 'Debe haber al menos un producto en su pedido antes de poder validarlo',
                });
                return false;
            }

            if (this.currentOrder.is_to_invoice() && !this.currentOrder.get_client()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: 'Por favor seleccione el Cliente',
                    body: 'Es necesario seleccionar el cliente antes de poder facturar un pedido.',
                });
                if (confirmed) {
                    this.selectClient();
                }
                return false;
            }

            let cliente = this.currentOrder.get_client();
            if (cliente) {
                if (cliente.l10n_mx_edi_addenda) {
                    if ( this.currentOrder.inputValue1 == false || this.currentOrder.inputValue1 == "" || this.currentOrder.inputValue1 == null ||
                         this.currentOrder.inputValue2 == false || this.currentOrder.inputValue2 == "" || this.currentOrder.inputValue2 == null ||
                         this.currentOrder.inputValue3 == false || this.currentOrder.inputValue3 == "" || this.currentOrder.inputValue3 == null ||
                         this.currentOrder.inputValue4 == false || this.currentOrder.inputValue4 == "" || this.currentOrder.inputValue4 == null){
                        this.showPopup('ErrorPopup', {
                            title: 'Faltan datos de la Addenda',
                            body: 'Los datos de la Addenda son obligatorios para este cliente.',
                        });
                        return false;
                    }
                }
            }

            if (!this.currentOrder.is_paid() || this.invoicing) {
                return false;
            }

            if (this.currentOrder.has_not_valid_rounding()) {
                var line = this.currentOrder.has_not_valid_rounding();
                this.showPopup('ErrorPopup', {
                    title: 'Redondeo incorrecto',
                    body: 'Usted debe redondear sus líneas de pago.' + line.amount + ' no está redondeado.',
                });
                return false;
            }

            // The exact amount must be paid if there is no cash payment method defined.
            if (
                Math.abs(
                    this.currentOrder.get_total_with_tax() - this.currentOrder.get_total_paid()  + this.currentOrder.get_rounding_applied()
                ) > 0.00001
            ) {
                var cash = false;
                for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
                    cash = cash || this.env.pos.payment_methods[i].is_cash_count;
                }
                if (!cash) {
                    this.showPopup('ErrorPopup', {
                        title: 'No se puede devolver cambio sin un método de pago de caja',
                        body: 'No hay ningún método de pago de caja disponible en este TPV para manejar el cambio.\n\n Pague el importe exacto o añada un método de pago de caja en la configuración del TPV',
                    });
                    return false;
                }
            }

            // if the change is too large, it's probably an input error, make the user confirm.
            if (
                !isForceValidate &&
                this.currentOrder.get_total_with_tax() > 0 &&
                this.currentOrder.get_total_with_tax() * 1000 < this.currentOrder.get_total_paid()
            ) {
                this.showPopup('ConfirmPopup', {
                    title: 'Porfavor Confirme Cantidad Grande',
                    body:
                        '¿Está seguro que el cliente quiere pagar' +
                        ' ' +
                        this.env.pos.format_currency(this.currentOrder.get_total_paid()) +
                        ' ' +
                        'una orden de' +
                        ' ' +
                        this.env.pos.format_currency(this.currentOrder.get_total_with_tax()) +
                        ' ' +
                        '? Dando click en "Confirmar" validara el pago.',
                }).then(({ confirmed }) => {
                    if (confirmed) this.validateOrder(true);
                });
                return false;
            }

            return true;
        }

    };

    Registries.Component.extend(PaymentScreen, LeyCustomPaymentScreen);
    return PaymentScreen;

});