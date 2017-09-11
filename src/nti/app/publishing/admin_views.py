#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from zope.cachedescriptors.property import Lazy

from zope.component.hooks import site as current_site

from zope.intid.interfaces import IIntIds

from ZODB.POSException import POSError

from pyramid.view import view_config
from pyramid.view import view_defaults

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.publishing import PublishingPathAdapter

from nti.dataserver.authorization import ACT_NTI_ADMIN

from nti.dataserver.interfaces import IDataserverFolder

from nti.dataserver.metadata.index import get_metadata_catalog

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.publishing.index import get_publishing_catalog

from nti.publishing.interfaces import get_publishables

from nti.site.hostpolicy import get_all_host_sites

ITEMS = StandardExternalFields.ITEMS
TOTAL = StandardExternalFields.TOTAL
ITEM_COUNT = StandardExternalFields.ITEM_COUNT


@view_config(context=IDataserverFolder)
@view_config(context=PublishingPathAdapter)
@view_defaults(route_name='objects.generic.traversal',
               renderer='rest',
               request_method='POST',
               permission=ACT_NTI_ADMIN,
               name='RebuildPublishingCatalog')
class RebuildPublishingCatalogView(AbstractAuthenticatedView):

    @Lazy
    def catalog(self):
        return get_publishing_catalog()

    @Lazy
    def metadata(self):
        return get_metadata_catalog()

    def __call__(self):
        catalog = self.catalog
        metadata = self.metadata
        for index in catalog.values():
            index.clear()
        # reindex
        seen = set()
        items = dict()
        intids = component.getUtility(IIntIds)
        for host_site in get_all_host_sites():  # check all sites
            with current_site(host_site):
                count = 0
                for publishable in get_publishables():
                    doc_id = intids.queryId(publishable)
                    if doc_id is None or doc_id in seen:
                        continue
                    try:
                        seen.add(doc_id)
                        catalog.force_index_doc(doc_id, publishable)
                        metadata.force_index_doc(doc_id, publishable)
                    except POSError:
                        logger.error("Error while indexing object %s/%s", 
                                     doc_id, type(publishable))
                    else:
                        count += 1
                items[host_site.__name__] = count
        result = LocatedExternalDict()
        result[ITEMS] = items
        result[ITEM_COUNT] = result[TOTAL] = len(seen)
        return result
