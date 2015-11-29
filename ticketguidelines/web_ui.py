# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 Sebastian Krysmanski
# Copyright (C) 2012 Greg Lavallee
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from genshi.builder import tag
from genshi.filters.transform import Transformer
from trac.core import *
from trac.web.api import IRequestFilter, ITemplateStreamFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet
from trac.wiki.formatter import format_to_html
from trac.wiki.model import WikiPage

NEW_TICKET_PAGE_NAME = 'TicketGuidelines/NewTicketSummary'
MODIFY_TICKET_PAGE_NAME = 'TicketGuidelines/ModifyTicketSummary'


def _get_wiki_html(env, data, is_new_ticket):
    wiki_page = is_new_ticket and NEW_TICKET_PAGE_NAME or \
                MODIFY_TICKET_PAGE_NAME
    page = WikiPage(env, wiki_page)
    if len(page.text) != 0:
        text = page.text
    else:
        if is_new_ticket:
            text = 'No ticket guidelines for creating a new ticket have ' \
                   'been specified. Please create [wiki:%s this wiki page] ' \
                   'to specify these guidelines.' \
                   % NEW_TICKET_PAGE_NAME
        else:
            text = 'No ticket guidelines for modifying a ticket have been ' \
                   'specified. Please create [wiki:%s this wiki page] to ' \
                   'specify these guidelines.' \
                   % MODIFY_TICKET_PAGE_NAME

    return tag.div(format_to_html(env, data['context'], text),
                   class_='ticket-guidelines')


class TicketGuidelinesContentProvider(Component):
    """This component provides the CSS file for the ticket guidelines box."""

    implements(ITemplateProvider, IRequestFilter)

    # ITemplateProvider methods

    def get_templates_dirs(self):
        return []

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [
            ('ticketguidelinesplugin', resource_filename(__name__, 'htdocs'))]

    # IRequestFilter methods

    def post_process_request(self, req, template, data, content_type):
        if template and (
                req.path_info.startswith('/ticket/') or
                req.path_info.startswith('/newticket')):
            add_stylesheet(req, 'ticketguidelinesplugin/main.css')

        return template, data, content_type

    def pre_process_request(self, req, handler):
        return handler


class NewTicketGuidelinesBox(Component):
    """ This component inserts the ticket guidelines hints for new into the
        ticket form.
    """

    implements(ITemplateStreamFilter)

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if method != 'xhtml':
            return stream

        if req.path_info.startswith('/newticket'):
            stream = stream | Transformer('//form[@id="propertyform"]').before(
                _get_wiki_html(self.env, data, True))

        return stream


class TicketCommentGuidelinesBox(Component):
    """ This component inserts the ticket guidelines hints for ticket
    comments into the ticket form.
    """

    implements(ITemplateStreamFilter)

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if method != 'xhtml':
            return stream

        if req.path_info.startswith('/ticket/'):
            stream = stream | Transformer('//form[@id="propertyform"]').before(
                _get_wiki_html(self.env, data, False))

        return stream
