#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from nti.app.publishing import TRX_TYPE_PUBLISH
from nti.app.publishing import TRX_TYPE_UNPUBLISH

from nti.externalization.internalization import notifyModified

from nti.publishing.interfaces import IPublishable
from nti.publishing.interfaces import ICalendarPublishable
from nti.publishing.interfaces import IObjectPublishedEvent
from nti.publishing.interfaces import IObjectUnpublishedEvent
from nti.publishing.interfaces import ICalendarPublishableModifiedEvent

from nti.recorder.interfaces import IRecordable

from nti.recorder.utils import record_transaction


@component.adapter(IPublishable, IObjectPublishedEvent)
def _record_published(obj, event):
    if IRecordable.providedBy(obj):
        record_transaction(obj, type_=TRX_TYPE_PUBLISH)


@component.adapter(IPublishable, IObjectUnpublishedEvent)
def _record_unpublished(obj, event):
    if IRecordable.providedBy(obj):
        record_transaction(obj, type_=TRX_TYPE_UNPUBLISH)


@component.adapter(ICalendarPublishable, ICalendarPublishableModifiedEvent)
def _on_calendar_publishable_modified(obj, event):
    notifyModified(obj, {u'publishBeginning': event.publishBeginning,
                         u'publishEnding': event.publishBeginning})