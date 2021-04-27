odoo.define('pos_addenda_custom.AdendaPopup', function(require) {
    'use strict';

    const { useState, useRef } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');


    class AdendaPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({
                inputValue1: this.props.startingValue1,
                inputValue2: this.props.startingValue2,
                inputValue3: this.props.startingValue3,
                inputValue4: this.props.startingValue4
            });
            this.inputRef = useRef('input');
        }
        mounted() {
            this.inputRef.el.focus();
        }
        getPayload() {
            return {
                inputValue1: this.state.inputValue1,
                inputValue2: this.state.inputValue2,
                inputValue3: this.state.inputValue3,
                inputValue4: this.state.inputValue4
            };
        }
    }
    AdendaPopup.template = 'AdendaPopup';
    AdendaPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: '',
        body: '',
        startingValue: '',
    };

    Registries.Component.add(AdendaPopup);

    return AdendaPopup;
});
