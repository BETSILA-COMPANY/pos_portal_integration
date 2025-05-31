/** @odoo-module **/

import { PosComponent } from 'point_of_sale.BaseComponent';
import Registries from 'point_of_sale.Registries';
import { ProductScreen } from 'point_of_sale.ProductScreen';

class PortalOrdersButton extends PosComponent {
    async onClick() {
        this.showPopup('ErrorPopup', {
            title: 'Coming Soon',
            body: 'This will show unpaid portal orders!',
        });
    }
}

PortalOrdersButton.template = 'PortalOrdersButton';

ProductScreen.addControlButton({
    component: PortalOrdersButton,
    condition: function () {
        return true;  // Always show for now
    },
    position: ['after', 'SetPartnerButton'],
});

Registries.Component.add(PortalOrdersButton);
