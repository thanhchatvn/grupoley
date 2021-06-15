odoo.define('pos_custom_promotions.PromoButton', function (require) {
    'use strict';

     const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

        class PromoButton extends PosComponent {
           constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        }
        PromoButton.template = 'PromoButton';
        ProductScreen.addControlButton({
        component: PromoButton,
        condition: function() {
            return this.env.pos.config.module_pos_pos_custom_promotions;
        },
    });

    Registries.Component.add(PromoButton);

    return PromoButton;
});
