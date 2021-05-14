odoo.define('pos_metodo_pago_cliente.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('res.partner', ['property_payment_term_id', 'x_l10n_mx_edi_payment_method_id']);

});