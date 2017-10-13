#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import greater_than_or_equal_to

from zope import component
from zope import interface

from nti.dataserver.interfaces import IDataserver

from nti.publishing.interfaces import IPublishable
from nti.publishing.interfaces import IPublishables

from nti.publishing.mixins import PublishableMixin

from nti.zodb.persistentproperty import PersistentPropertyHolder

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver


@interface.implementer(IPublishable)
class Bleach(PersistentPropertyHolder, PublishableMixin):
    pass


class TestAdminViews(ApplicationLayerTest):

    @WithSharedApplicationMockDS(users=True, testapp=True)
    def test_rebuild_catalog(self):
        with mock_dataserver.mock_db_trans(self.ds):
            bleach = Bleach()
            current_transaction = mock_dataserver.current_transaction
            current_transaction.add(bleach)
            self.ds.root['bleach'] = bleach

        class _global_recs(object):
            def iter_objects(self):
                dataserver = component.getUtility(IDataserver)
                yield dataserver.root['bleach']

        utility = _global_recs()
        gsm = component.getGlobalSiteManager()
        gsm.registerUtility(utility, IPublishables, "bleach")
        try:
            res = self.testapp.post('/dataserver2/publishing/@@RebuildPublishingCatalog',
                                    status=200)
            assert_that(res.json_body,
                        has_entries('Total', is_(greater_than_or_equal_to(1)),
                                    'ItemCount', is_(greater_than_or_equal_to(1))))
        finally:
            gsm.unregisterUtility(utility, IPublishables, "bleach")
