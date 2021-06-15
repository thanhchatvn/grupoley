odoo.define("pos_custom_promotions.models", function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');

    var field_utils = require('web.field_utils');
    models.load_fields('pos.order.line',['discount_rate','discount_promotions','is_discount_calculated','discount_original']);
    var super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var pos_order_line_model = _.find(this.models, function (model){
                return model.model === 'pos.order.line';
            });
            pos_order_line_model.fields.push('discount_rate','discount_promotions','is_discount_calculated','discount_original');
            return super_posmodel.initialize.call(this, session, attributes);
        },
    });
});