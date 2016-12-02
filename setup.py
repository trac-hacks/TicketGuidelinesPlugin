# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 Sebastian Krysmanski
# Copyright (C) 2012 Greg Lavallee
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from setuptools import setup

PACKAGE = 'TicketGuidelinesPlugin'
VERSION = '1.0.0'

setup(
    name=PACKAGE,
    version=VERSION,
    author='Sebastian Krysmanski',
    url='https://github.com/trac-hacks/TicketGuidelinesPlugin',
    description="Adds your ticket guidelines to the ticket view. The "
                "guidelines are specified in the wiki pages "
                "'TicketGuidelines/NewShort' and "
                "'TicketGuidelines/ModifyShort'.",
    keywords='trac plugin',
    license='Modified BSD',
    install_requires=['Trac'],
    packages=['ticketguidelines'],
    package_data={'ticketguidelines': ['htdocs/*']},
    entry_points={'trac.plugins': '%s = ticketguidelines.web_ui' % PACKAGE},
)
