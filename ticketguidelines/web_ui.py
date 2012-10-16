# -*- coding: utf-8 -*-
#
#            Copyright (C) 2009 Massive Trac Provider Project
#
#                         All rights reserved.
#
################################################################################
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. The name of the author may not be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR `AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
################################################################################
# 
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at: https://svn.mayastudios.de/mtpp/log/
#
# Author: Sebastian Krysmanski
#
################################################################################
#
# $Revision: 302 $
# $Date: 2009-09-04 13:37:44 +0000 (Fri, 04 Sep 2009) $
# $URL: https://svn.mayastudios.de/mtpp/repos/plugins/ticketguidelines/trunk/ticketguidelines/web_ui.py $
#
################################################################################

from trac.core import *
from trac.web.api import IRequestFilter, ITemplateStreamFilter
from trac.web.chrome import add_stylesheet, ITemplateProvider

from trac.wiki.model import WikiPage
from trac.wiki.formatter import format_to_html

from genshi.builder import tag
from genshi.filters.transform import Transformer

NEW_TICKET_PAGE_NAME = 'TicketGuidelines/NewTicketSummary'
MODIFY_TICKET_PAGE_NAME = 'TicketGuidelines/ModifyTicketSummary'

def _get_wiki_html(env, data, is_new_ticket):
  wiki_page = is_new_ticket and NEW_TICKET_PAGE_NAME or MODIFY_TICKET_PAGE_NAME
  page = WikiPage(env, wiki_page)
  if len(page.text) != 0:
    text = page.text
  else:
    if is_new_ticket:
      text = 'No ticket guidelines for creating a new ticket have been specified. ' \
             'Please create [wiki:%s this wiki page] to specify these guidelines.' \
             % NEW_TICKET_PAGE_NAME
    else:
      text = 'No ticket guidelines for modifying a ticket have been specified. ' \
             'Please create [wiki:%s this wiki page] to specify these guidelines.' \
             % MODIFY_TICKET_PAGE_NAME
  
  return tag.div(format_to_html(env, data['context'], text), class_='ticket-guidelines')

class TicketGuidelinesContentProvider(Component):
  """ This component provides the CSS file for the ticket guidelines box. """

  implements(ITemplateProvider, IRequestFilter)
  
  # ITemplateProvider methods
  def get_templates_dirs(self):
    """Return a list of directories containing the provided template files.
    """  
    return []

  def get_htdocs_dirs(self):
    """ Return a list of directories with static resources (such as style
        sheets, images, etc.)

        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.
      
        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
    """
    from pkg_resources import resource_filename
    return [('ticketguidelinesplugin', resource_filename(__name__, 'htdocs'))]
    
  # IRequestFilter methods
  
  def post_process_request(self, req, template, data, content_type):
    """Do any post-processing the request might need; typically adding
    values to the template `data` dictionary, or changing template or
    mime type.
    
    `data` may be update in place.

    Always returns a tuple of (template, data, content_type), even if
    unchanged.

    Note that `template`, `data`, `content_type` will be `None` if:
     - called when processing an error page
     - the default request handler did not return any result

    (Since 0.11)
    """
    
    if template and (req.path_info.startswith('/ticket/') or req.path_info.startswith('/newticket')):
      add_stylesheet(req, 'ticketguidelinesplugin/main.css')
      
    return (template, data, content_type)

  def pre_process_request(self, req, handler):
    """Called after initial handler selection, and can be used to change
    the selected handler or redirect request.
    
    Always returns the request handler, even if unchanged.
    """
    return handler
    
class NewTicketGuidelinesBox(Component):
  """ This component inserts the ticket guidelines hints for new into the 
      ticket form. 
  """

  implements(ITemplateStreamFilter)
  
  # ITemplateStreamFilter methods
    
  def filter_stream(self, req, method, filename, stream, data):
    """Return a filtered Genshi event stream, or the original unfiltered
    stream if no match.

    `req` is the current request object, `method` is the Genshi render
    method (xml, xhtml or text), `filename` is the filename of the template
    to be rendered, `stream` is the event stream and `data` is the data for
    the current template.

    See the Genshi documentation for more information.
    """
    if method != 'xhtml':
      return stream
      
    if req.path_info.startswith('/newticket'):
      stream = stream | Transformer('//form[@id="propertyform"]').before(_get_wiki_html(self.env, data, True))
      
    return stream

class TicketCommentGuidelinesBox(Component):
  """ This component inserts the ticket guidelines hints for ticket comments 
      into the ticket form. 
  """

  implements(ITemplateStreamFilter)
  
  # ITemplateStreamFilter methods
    
  def filter_stream(self, req, method, filename, stream, data):
    """Return a filtered Genshi event stream, or the original unfiltered
    stream if no match.

    `req` is the current request object, `method` is the Genshi render
    method (xml, xhtml or text), `filename` is the filename of the template
    to be rendered, `stream` is the event stream and `data` is the data for
    the current template.

    See the Genshi documentation for more information.
    """
    if method != 'xhtml':
      return stream
      
    if req.path_info.startswith('/ticket/'):
      stream = stream | Transformer('//form[@id="propertyform"]').before(_get_wiki_html(self.env, data, False))
      
    return stream
