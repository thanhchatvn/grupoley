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
                        if (orderlines[i].discount){
                            es_bloqueado = true;
                            motivo += 'Se ha ingresado un descuento de ' + orderlines[i].discount + '% para el producto ' + orderlines[i].product.display_name + '. '
                        }
                        let precio = orderlines[i].product.get_price(this.currentOrder.pricelist, 1)
                        if (precio != orderlines[i].price){
                            es_bloqueado = true;
                            motivo += 'Se ha cambiado el precio a ' + orderlines[i].price + ' del producto ' + orderlines[i].product.display_name + '. '
                        }
                    }
                    if (es_bloqueado) {
                        let self = this
                        if (this.currentOrder.autorizacion){
                            let autorizacion = this.currentOrder.autorizacion
                            const result = await this.rpc({
                                model: 'pos.autorizacion',
                                method: 'revisar_estado',
                                args: [autorizacion],
                            })
                            if (result == 'pendiente'){
                                self.showPopup('ErrorPopup', {
                                    title: 'Venta bloqueada',
                                    body: 'Esta venta requiere de autorización.',
                                });
                                return false;
                            } else if (result == 'aprobado'){
                                self.currentOrder.autorizacion = null;
                                let detalles = []
                                for (var i = 0; i < orderlines.length; i++) {
                                    detalles.push([{
                                        'product_id': orderlines[i].product.id,
                                        'cantidad': orderlines[i].quantity,
                                        'unitario': orderlines[i].price,
                                        'descuento': orderlines[i].discount,
                                    }]);
                                }
                                const comprobar = await this.rpc({
                                    model: 'pos.autorizacion',
                                    method: 'comprobar',
                                    args: [[autorizacion], {
                                        'partner_id': cliente.id,
                                        'pricelist_id': self.currentOrder.pricelist.id,
                                        'detalles': detalles,
                                    }],
                                })
                                if (comprobar){
                                    return true;
                                } else {
                                    self.showPopup('ErrorPopup', {
                                        title: 'Venta modificada',
                                        body: 'La autorización aprobada y la presente venta presentan diferencias.',
                                    });
                                    return false;
                                }
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