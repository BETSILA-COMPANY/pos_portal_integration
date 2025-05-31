Odoo POS Portal Integration Module Name: pos_portal_integration Version:
16.0.1.0.0 Author: BETSILA AND COMPANY License: LGPL-3

🚀 Overview The POS Portal Integration module empowers your Odoo Point
of Sale (POS) system by enabling registered customers to create and
manage their POS orders directly from their personalized customer
portal. This solution streamlines the ordering process, enhances
customer convenience, and reduces the manual workload for your POS
staff.

✨ Key Features Customer Self-Service Ordering: Provide an intuitive
interface on the customer portal where users can easily browse products,
select quantities, and submit new POS orders.

Real-time Product Availability: Customers can view products marked as
\"Available in PoS\" from your Odoo product catalog.

Automatic Pricing & Tax Calculation: Orders placed through the portal
automatically respect customer-specific pricelists and apply relevant
taxes based on your Odoo\'s accounting configuration (including fiscal
positions if configured).

Direct POS Order Creation: Submitted orders are seamlessly created as
Draft POS Orders directly within your Odoo backend, ready for your POS
staff to process.

Portal Order History: Customers gain access to a dedicated section in
their portal dashboard to view the status and details of all their past
POS orders.

Seamless Odoo Integration: Designed to integrate flawlessly with Odoo\'s
native portal and Point of Sale modules, ensuring a consistent user
experience.

🌟 Benefits Enhanced Customer Satisfaction: Offer 24/7 self-service
capabilities, improving convenience and accessibility for your
customers.

Increased Operational Efficiency: Reduce manual order entry and free up
your POS staff to focus on customer service.

Streamlined Order Management: Automate the flow from customer order
submission to POS order creation.

Improved Order Accuracy: Minimize errors associated with manual
transcription of orders.

Scalability: Easily handle increased order volumes without proportional
increases in staff workload.

🛠️ Installation Clone the Repository: Navigate to your Odoo custom
addons directory (e.g., /opt/odoo16/addons/) and clone this repository:

cd /opt/odoo16/addons/ git clone
https://github.com/BETSILA-COMPANY/pos_portal_integration.git

(If you\'ve already cloned it, ensure your local copy is up-to-date with
git pull origin main)

Update Odoo Modules List:

Restart your Odoo server to recognize the new module.

sudo systemctl restart odoo16

In Odoo, navigate to Apps -\> Update Apps List (you might need to remove
the \"Apps\" filter first).

Install the Module:

Search for \"POS Portal Integration\" in the Odoo Apps menu.

Click the \"Install\" button.

⚙️ Configuration POS Configuration:

Ensure you have at least one active Point of Sale Configuration (Point
of Sale -\> Configuration -\> Point of Sale).

Verify that a Pricelist is associated with your POS Configuration.

Ensure there is an Opened POS Session for orders to be created.

Product Configuration:

For any product you wish to make available for ordering through the
portal, navigate to its form view (Sales -\> Products -\> Products).

Under the Point of Sale tab, ensure the \"Available in PoS\" checkbox is
ticked.

Verify that products have appropriate Customer Taxes configured under
the Sales tab.

Company Tax Configuration:

Go to Settings -\> Companies -\> Your Company.

Under the Accounting tab, ensure a \"Default Sales Tax\" is selected.
Even a 0% tax helps Odoo\'s tax engine.

Fiscal Positions (Optional but Recommended):

If you deal with different tax rules based on customer location,
configure your Fiscal Positions (Accounting -\> Configuration -\> Fiscal
Positions).

Ensure your customer records (Contacts -\> Customers) have the correct
Fiscal Position assigned under the Sales & Purchase tab.

📝 Usage Customer Login:

Customers log in to their Odoo portal account (e.g., your_odoo_url/my).

Access POS Orders:

On the portal dashboard, they will find a new section or link for \"My
POS Orders\".

Create New Order:

Click \"Create New POS Order\".

Select the desired products and specify quantities.

Click \"Confirm Order\".

View Orders:

After creation, the customer is redirected to their \"My POS Orders\"
list, where they can see their newly created order and its status.

They can click on an order to view its details.

POS Backend Processing:

In the Odoo backend, your POS staff can navigate to Point of Sale -\>
Orders.

The portal-submitted orders will appear here as Draft orders, ready to
be validated and processed.

🤝 Support For any questions, issues, or custom development requests,
please contact us:

Email: mahokazsilas@example.com

📄 License This module is licensed under the LGPL-3.0. See the LICENSE
file in this repository for full details.
