#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

from zope import component

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver

from nti.publishing.interfaces import IPublishables


class TestPublishables(ApplicationLayerTest):

    @WithSharedApplicationMockDS(users=True, testapp=True)
    def test_publishables(self):

        with mock_dataserver.mock_db_trans(self.ds):
            publishables = component.queryUtility(IPublishables, "entities")
            assert_that(publishables, is_not(none()))
            assert_that(list(publishables.iter_objects()),
                        has_length(0))
