odoo.define('pos_autorizacion.PaymentScreen', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    models.load_fields('res.partner', ['credit_limit', 'total_overdue']);

    const PosAutorizacionPaymentScreen = (PaymentScreen) => class extends PaymentScreen {

        async _isOrderValid(isForceValidate) {
            let valido = await super._isOrderValid(...arguments);
            if (valido) {
                let cliente = this.currentOrder.get_client();
                if (cliente) {
                    let es_bloqueado = false;
                    let motivo = '';
                    if (cliente.credit_limit) {
                        if (cliente.credit_limit - cliente.total_overdue - this.currentOrder.get_total_with_tax() - this.currentOrder.get_rounding_applied() < 0){
                            es_bloqueado = true;
                            motivo += 'Excede límite de crédito. '
                        }
                    }
                    let orderlines = this.currentOrder.orderlines.models
                    for (var i = 0; i < orderlines.length; i++){
                        if (orderlines[0].discount){
                            es_bloqueado = true;
                            motivo += 'Se ha ingresado un descuento de ' + orderlines[0].discount + '% para el producto ' + orderlines[0].product.display_name + '. '
                        }
                        let precio = orderlines[0].product.get_price(this.currentOrder.pricelist, 1)
                        if (precio != orderlines[0].price){
                            es_bloqueado = true;
                            motivo += 'Se ha cambiado el precio a ' + orderlines[0].price + ' del producto ' + orderlines[0].product.display_name + '. '
                        }
                    }

                    if (es_bloqueado) {
                        let self = this
                        if (this.currentOrder.autorizacion){
                            const result = await this.rpc({
                                model: 'pos.autorizacion',
                                method: 'revisar_estado',
                                args: [this.currentOrder.autorizacion],
                            })
                            if (result == 'pendiente'){
                                self.showPopup('ErrorPopup', {
                                    title: 'Venta bloqueada',
                                    body: 'Esta venta requiere de autorización.',
                                });
                                return false;
                            } else if (result == 'aprobado'){
                                self.currentOrder.autorizacion = null;
                                return true;
                            } else if (result == 'rechazado'){
                                self.showPopup('ErrorPopup', {
                                    title: 'Venta bloqueada',
                                    body: 'La autorización ha sido rechazada.',
                                });
                                self.currentOrder.autorizacion = null;
                                return false;
                            }
                        } else {
                            this.showPopup('ErrorPopup', {
                                title: 'Venta bloqueada',
                                body: 'Esta venta requiere de autorización.',
                            });
                            let detalles = []
                            for (var i = 0; i < orderlines.length; i++) {
                                let impuestos = []
                                for (var j = 0; j < orderlines[i].product.taxes_id.length; j++){
                                    impuestos.push([4, orderlines[i].product.taxes_id[j]])
                                }
                                detalles.push([0, 0, {
                                    'product_id': orderlines[i].product.id,
                                    'cantidad': orderlines[i].quantity,
                                    'unitario': orderlines[i].price,
                                    'descuento': orderlines[i].discount,
                                    'impuesto': impuestos,
                                }]);
                            }
                            this.rpc({
                                model: 'pos.autorizacion',
                                method: 'create',
                                args: [{
                                    'name': this.currentOrder.name,
                                    'partner_id': cliente.id,
                                    'user_id': this.currentOrder.employee.user_id[0],
                                    'pricelist_id': this.currentOrder.pricelist.id,
                                    'detalle_ids': detalles,
                                    'motivo': motivo,
                                }],
                            }).then(function (result) {
                                self.currentOrder.autorizacion = result;
                            });
                        }

                        return false;
                    }
                }
            }
            return valido
        }
    };

    Registries.Component.extend(PaymentScreen, PosAutorizacionPaymentScreen);
    return PaymentScreen;

});