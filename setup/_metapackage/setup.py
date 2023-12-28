import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-mia",
    description="Meta package for open-synergy-opnsynid-mia Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_mia_absen_harian_py3o_report',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
