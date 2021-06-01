odoo.define('pos_lista_precio.SetPricelistButton', function (require) {
    "use strict";

    const SetPricelistButton = require('point_of_sale.SetPricelistButton');
    const Registries = require('point_of_sale.Registries');

    const PosListaPrecioSetPricelistButton = (SetPricelistButton) => class extends SetPricelistButton {
        async onClick() {
            let cliente = this.currentOrder.get_client();
            if (cliente) {
                const selectionList = this.env.pos.pricelists.filter(e => e.id == cliente.property_product_pricelist[0]).map(pricelist => ({
                    id: pricelist.id,
                    label: pricelist.name,
                    isSelected: pricelist.id === this.currentOrder.pricelist.id,
                    item: pricelist,
                }));

                const { confirmed, payload: selectedPricelist } = await this.showPopup(
                    'SelectionPopup',
                    {
                        title: this.env._t('Select the pricelist'),
                        list: selectionList,
                    }
                );

                if (confirmed) {
                    this.currentOrder.set_pricelist(selectedPricelist);
                }
            } else {
                this.showPopup('ErrorPopup', {
                    title: 'Seleccionar cliente',
                    body: 'Por favor seleccionar cliente antes de cambiar de tarifa.',
                });
            }
        }
    };

    Registries.Component.extend(SetPricelistButton, PosListaPrecioSetPricelistButton);
    return SetPricelistButton;

});