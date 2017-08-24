Plant Nursery Module
====================

This module is a simple usecase to present the Odoo framework during the
Odoodays 2019.

See the [commit history](https://github.com/tivisse/odoodays-2019/commits/master/)
to follow the evolution of the module.

See the full presentations [here](https://github.com/tivisse/odooplants/tree/13.0/plant_nursery/static/pdf)

Note:
To be able to install the module nursery_plant_data, either you have to create the
following untracked files and add your credentials to test the mail and sms
gateways, or to comment the import in the ``__manifest__.py`` file.

- 'data/mail_data.xml',  # to define manually
- 'data/contact_private_data.xml',  # to define manually
- 'data/sms_private_data.xml',  # to define manually
- 'data/gateway_private_data.xml',  # to define manually
- 'data/contact_private_demo.xml',  # to define manually
