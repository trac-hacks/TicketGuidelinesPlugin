from setuptools import setup

PACKAGE = 'TicketGuidelinesPlugin'
VERSION = '0.1'

setup(
    name = PACKAGE,
    version = VERSION,
    
    author = "Sebastian Krysmanski",
    author_email = None,
    url = "https://svn.mayastudios.de/mtpp/wiki/Plugins/TicketGuidelinesPlugin",
    
    description = "Adds your ticket guidelines to the ticket view. The guidelines " \
                  "are specified in the wiki pages 'TicketGuidelines/NewShort' and " \
                  "'TicketGuidelines/ModifyShort'.",
    keywords = "trac plugins",
    
    license = "Modified BSD",
    
    install_requires = [
        'Trac>=0.11',
    ],
    
    packages = ['ticketguidelines'],
    package_data = { 'ticketguidelines': [ 'htdocs/*' ] },
                                     
    entry_points = { 'trac.plugins': '%s = ticketguidelines.web_ui' % PACKAGE },
)