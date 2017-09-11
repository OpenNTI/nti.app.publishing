#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory('nti.dataserver')

from zope import interface

from zope.location.interfaces import IContained

from zope.traversing.interfaces import IPathAdapter

#: Publish view name
VIEW_PUBLISH = "publish"

#: Unpublish view name
VIEW_UNPUBLISH = "unpublish"

#: Publish transaction type
TRX_TYPE_PUBLISH = u'publish'

#: Unpublish transaction type
TRX_TYPE_UNPUBLISH = u'unpublish'

#: Publishing path adapter
PUBLISHING_ADAPTER = 'publishing'


@interface.implementer(IPathAdapter, IContained)
class PublishingPathAdapter(object):

    __name__ = PUBLISHING_ADAPTER

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
