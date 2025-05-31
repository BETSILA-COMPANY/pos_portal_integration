odoo.define('pos_portal_integration.PortalOrders', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class PortalOrderButton extends PosComponent {
        async onClick() {
            const orders = await this.rpc({
                model: 'pos.order',
                method: 'search_read',
                args: [[['portal_state', '=', 'submitted']]],
            });
            
            // Show orders in a popup for selection
            // Implementation depends on your specific UI requirements
        }
    }
    PortalOrderButton.template = 'PortalOrderButton';
    Registries.Component.add(PortalOrderButton);

    return {
        PortalOrderButton,
    };
});
