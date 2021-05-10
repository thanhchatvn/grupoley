odoo.define('pos_cliente_almacen.ClientListScreen', function (require) {
    "use strict";

    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');

    models.load_fields('res.partner', 'property_warehouse_id');

    const PosClienteAlmacenClientListScreen = (ClientListScreen) => class extends ClientListScreen {
        get clients() {
            if (this.state.query && this.state.query.trim() !== '') {
                let warehouse_id = this.env.pos.config.property_warehouse_id[0]
                let clientes = this.env.pos.db.search_partner(this.state.query.trim()).filter(e => e.property_warehouse_id[0] == warehouse_id);
                return clientes;
            } else {
                let warehouse_id = this.env.pos.config.property_warehouse_id[0]
                let clientes = this.env.pos.db.get_partners_sorted(1000).filter(e => e.property_warehouse_id[0] == warehouse_id);
                return clientes;
            }
        }
        get nextButton() {
            if (!this.props.client) {
                return { command: 'set', text: 'Seleccionar Cliente' };
            } else if (this.props.client && this.props.client === this.state.selectedClient) {
                return { command: 'deselect', text: 'Deseleccionar Cliente' };
            } else {
                return { command: 'set', text: 'Cambiar Cliente' };
            }
        }
    };

    Registries.Component.extend(ClientListScreen, PosClienteAlmacenClientListScreen);
    return ClientListScreen;

});