odoo.define("pos_cantidad_stock.PosModel", function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');
    var field_utils = require('web.field_utils');

    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_product_model: function() {
            return _.find(this.models, function(model) {
                return model.model === "product.product";
            });
        },
        initialize: function(session, attributes) {
            this.product_product_model = this.get_product_model(this.models);
            PosModelSuper.initialize.apply(this, arguments);
        },
        load_server_data: function() {
            var self = this;
            var loaded = PosModelSuper.load_server_data.call(this);
            return loaded.then(function() {
                return rpc
                    .query({
                        model: "product.product",
                        method: "prueba",
                        args: ["", self.config.default_location_src_id[0]],
                        fields: ["qty_available"],
                        domain: self.product_product_model.domain,
                        context: _.extend(self.product_product_model.context, {
                            location: self.config.default_location_src_id[0],
                        }),
                    })
                    .then(function(products) {
                        self.add_product_qty(products);
                    });
            });
        },
        set_product_qty_available: function(product, qty) {
            product.qty_available = qty;
            this.refresh_qty_available(product);
        },
        update_product_qty_from_order_lines: function(order) {
            var self = this;
            order.orderlines.each(function(line) {
                var product = line.get_product();
                product.qty_available = product.format_float_value(
                    product.qty_available - line.get_quantity(),
                    {digits: [69, 3]}
                );
                self.refresh_qty_available(product);
            });
            // esta huevada esta por las puras!!!
            order.trigger("new_updates_to_send");
        },
        add_product_qty: function(products) {
            var self = this;
            _.each(products, function(p) {
                _.extend(self.db.get_product_by_id(p.id), p);
            });
        },
        refresh_qty_available: function(product) {
            var $elem = $("[data-product-id='" + product.id + "'] .qty-tag");
            $elem.html(product.rounded_qty());
            if (product.qty_available <= 0 && !$elem.hasClass("not-available")) {
                $elem.addClass("not-available");
            }
        },
        push_orders: function(order, opts) {
            var pushed = PosModelSuper.push_orders.call(this, order, opts);
            if (order) {
                this.update_product_qty_from_order_lines(order);
            }
            return pushed;
        },
        push_and_invoice_order: function(order) {
            var invoiced = PosModelSuper.push_and_invoice_order.call(this, order);

            if (order && order.get_client() && order.orderlines) {
                this.update_product_qty_from_order_lines(order);
            }

            return invoiced;
        },
    });

    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
        export_as_JSON: function() {
            var data = OrderlineSuper.prototype.export_as_JSON.apply(this, arguments);
            data.qty_available = this.product.qty_available;
            return data;
        },
        // Compatibility with pos_multi_session
        apply_ms_data: function(data) {
            if (OrderlineSuper.prototype.apply_ms_data) {
                OrderlineSuper.prototype.apply_ms_data.apply(this, arguments);
            }
            var product = this.pos.db.get_product_by_id(data.product_id);
            if (product.qty_available !== data.qty_available) {
                this.pos.set_product_qty_available(product, data.qty_available);
            }
        },
    });

    models.Product = models.Product.extend({
        format_float_value: function(val) {
            var value = parseFloat(val);
            value = field_utils.format.float(value, {digits: [69, 3]});
            return String(parseFloat(value));
        },
        rounded_qty: function() {
            return this.format_float_value(this.qty_available);
        },
    });
});