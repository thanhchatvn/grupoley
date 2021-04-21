odoo.define('pos_addenda_custom.adenda', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var order_super = models.Order.prototype;

    models.load_fields('res.partner','l10n_mx_edi_addenda');

    models.Order = models.Order.extend({
        set_adenda: function(adenda) {
            this.inputValue1 = adenda['inputValue1']
            this.inputValue2 = adenda['inputValue2']
            this.inputValue3 = adenda['inputValue3']
            this.inputValue4 = adenda['inputValue4']
        },
        init_from_JSON: function(json) {
            order_super.init_from_JSON.apply(this, arguments);
            this.inputValue1 = json.inputValue1 || false;
            this.inputValue2 = json.inputValue2 || false;
            this.inputValue3 = json.inputValue3 || false;
            this.inputValue4 = json.inputValue4 || false;
        },
        export_as_JSON: function() {
            var json = order_super.export_as_JSON.apply(this, arguments);
            return _.extend(json, {
                'inputValue1': this.inputValue1,
                'inputValue2': this.inputValue2,
                'inputValue3': this.inputValue3,
                'inputValue4': this.inputValue4
            });
        }

    });

});