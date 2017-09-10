#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

from zope import component

from nti.publishing.interfaces import IPublishables

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver


class TestPublishables(ApplicationLayerTest):

    @WithSharedApplicationMockDS(users=True, testapp=True)
    def test_publishables(self):

        with mock_dataserver.mock_db_trans(self.ds):
            publishables = component.queryUtility(IPublishables, "entities")
            assert_that(publishables, is_not(none()))
            assert_that(list(publishables.iter_objects()),
                        has_length(0))
