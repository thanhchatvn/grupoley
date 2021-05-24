odoo.define('pos_addenda_custom.LeyCustomPaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const LeyCustomPaymentScreen = (PaymentScreen) => class extends PaymentScreen {

        async addAdenda() {
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
            let valido = await super._isOrderValid(...arguments);
            if (valido) {
                let cliente = this.currentOrder.get_client();
                let parent = false;
                if (cliente) {
                    if (cliente.parent_id){
                        const result = await this.rpc({
                            model: 'pos.order',
                            method: 'buscar_addenda_parent',
                            args: [[], cliente.parent_id[0]],
                        });
                        if (result){
                            parent = true;
                        }
                    }
                    if (cliente.l10n_mx_edi_addenda || parent) {
                        if ( this.currentOrder.inputValue1 == false || this.currentOrder.inputValue1 == "" || this.currentOrder.inputValue1 == null ||
                             this.currentOrder.inputValue2 == false || this.currentOrder.inputValue2 == "" || this.currentOrder.inputValue2 == null ||
                             this.currentOrder.inputValue3 == false || this.currentOrder.inputValue3 == "" || this.currentOrder.inputValue3 == null ||
                             this.currentOrder.inputValue4 == false || this.currentOrder.inputValue4 == "" || this.currentOrder.inputValue4 == null){
                            this.showPopup('ErrorPopup', {
                                title: 'Faltan datos de la Addenda',
                                body: 'Los datos de la Addenda son obligatorios para este cliente.',
                            });
                            return false;
                        } else {
                            return true;
                        }
                    } else {
                        return true;
                    }
                }
            } else {
                return false;
            }
        }

    };

    Registries.Component.extend(PaymentScreen, LeyCustomPaymentScreen);
    return PaymentScreen;

});