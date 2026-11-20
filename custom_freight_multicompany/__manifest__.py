{
    "name": "Custom Freight Multicompany",
    "version": "19.0.1.0.0",
    "summary": "Add a company field to the freight booking and shipment models.",
    "category": "Industry",
    "author": "Grupo Sachman",
    "depends": ["bi_freight_management"],
    "data": [
        "security/freight_security.xml",
        "views/freight_company_views.xml",
    ],
    "license": "OPL-1",
    "installable": True,
    'application': False,
}
