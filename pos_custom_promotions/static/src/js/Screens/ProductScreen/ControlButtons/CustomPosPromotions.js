odoo.define('pos_custom_promotions.CustomPosPromotions', function (require) {
    'use strict';
    alert(aqui)

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class CustomPosPromotions extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const { confirmed, payload: code } = await this.showPopup('TextInputPopup', {
                title: this.env._t('Check Promotions'),
                startingValue: '',
            });
        }
    }
    CustomPosPromotions.template = 'CustomPosPromotions';

    ProductScreen.addControlButton({
        component: CustomPosPromotions,
        condition: function () {
            return this.env.pos.config.module_pos_custom_promotions;
        },
    });

    Registries.Component.add(CustomPosPromotions);

    return CustomPosPromotions;
});
