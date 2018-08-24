#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from ZODB.POSException import POSError

from zope import component

from zope.component.hooks import site as current_site

from zope.intid.interfaces import IIntIds

from nti.dataserver.metadata.index import get_metadata_catalog

from nti.publishing.index import get_publishing_catalog

from nti.publishing.interfaces import get_publishables

from nti.site.hostpolicy import get_all_host_sites

logger = __import__('logging').getLogger(__name__)


def rebuild_publishing_catalog(seen=None, metadata=True):
    catalog = get_publishing_catalog()
    for index in catalog.values():
        index.clear()
    # reindex
    items = dict()
    seen = set() if seen is None else seen
    metadata_catalog = get_metadata_catalog()
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
                    catalog.index_doc(doc_id, publishable)
                    if metadata:
                        metadata_catalog.index_doc(doc_id, publishable)
                except POSError:
                    logger.error("Error while indexing object %s/%s",
                                 doc_id, type(publishable))
                else:
                    count += 1
            logger.info("%s object(s) indexed in site %s",
                        count, host_site.__name__)
            items[host_site.__name__] = count
    return items
