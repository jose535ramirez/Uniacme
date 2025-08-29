# -*- coding: utf-8 -*-

{
    "name": "UNIACME",
    "author": "Jose Ramirez",
    "version": "18.0.1.0.0",
    "website": "https://github.com/jose535ramirez",
    "license": "LGPL-3",
    "category": "Uncategorized",
    "depends": [
        "base",
        "contacts",
        "mail",
        "website",
    ],
    "summary": "UNIACME",
    "data": [
        "security/ir.model.access.csv",
        "views/headquarter_views.xml",
        "views/career_views.xml",
        "views/res_partner_view.xml",
        "views/voting_process_views.xml",
        "views/base_menus.xml",
        "views/vote_template.xml",
        "views/website_menu.xml",
        "wizard/voting_process_import_wizard.xml",
    ],
    "qweb": [
        "views/vote_template.xml",
    ],
    "installable": True,
    "auto_install": False,
}