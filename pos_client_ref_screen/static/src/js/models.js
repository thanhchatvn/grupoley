odoo.define("pos_client_ref_screen.models", function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');

    var field_utils = require('web.field_utils');
    models.load_fields('res.partner','ref');
    var super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function (model){
                return model.model === 'res.partner';
            });
            partner_model.fields.push('ref','category_id');
            return super_posmodel.initialize.call(this, session, attributes);
        },
    });
});