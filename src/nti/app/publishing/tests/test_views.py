#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable

from nti.app.publishing import TRX_TYPE_PUBLISH
from nti.app.publishing import TRX_TYPE_UNPUBLISH

from nti.base.interfaces import ICreated

from nti.dataserver.users import User

from nti.externalization.interfaces import IInternalObjectExternalizer

from nti.ntiids.oids import to_external_ntiid_oid

from nti.publishing.mixins import PublishableMixin

from nti.recorder.interfaces import ITransactionRecordHistory

from nti.recorder.mixins import RecordableMixin

from nti.zodb.persistentproperty import PersistentPropertyHolder

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver


@interface.implementer(ICreated, 
                       IAttributeAnnotatable,
                       IInternalObjectExternalizer)
class Bleach(PersistentPropertyHolder, 
             RecordableMixin,
             PublishableMixin):

    __name__ = None
    __parent__ = None
    
    def toExternalObject(self, **unused_kwargs):
        return {'Class':'Bleach'}


class TestViews(ApplicationLayerTest):

    def _create_ichigo(self):
        user = User.get_user(self.default_username)
        ichigo = Bleach()
        current_transaction = mock_dataserver.current_transaction
        current_transaction.add(ichigo)
        self.ds.root['ichigo'] = ichigo
        ichigo.creator = user
        return ichigo

    @WithSharedApplicationMockDS(users=True, testapp=True)
    def test_publish_unpublish(self):
        with mock_dataserver.mock_db_trans(self.ds):
            ichigo = self._create_ichigo()
            oid = to_external_ntiid_oid(ichigo)

        url = '/dataserver2/Objects/%s/@@publish' % oid
        self.testapp.post(url, status=200)
        
        with mock_dataserver.mock_db_trans(self.ds):
            ichigo = self.ds.root['ichigo']
            assert_that(ichigo.is_published(), is_(True))
            history = ITransactionRecordHistory(ichigo)
            record = history.query(record_type=TRX_TYPE_PUBLISH)
            assert_that(record, is_not(none()))

        url = '/dataserver2/Objects/%s/@@unpublish' % oid
        self.testapp.post(url, status=200)
        with mock_dataserver.mock_db_trans(self.ds):
            ichigo = self.ds.root['ichigo']
            assert_that(ichigo.is_published(), is_(False))
            history = ITransactionRecordHistory(ichigo)
            record = history.query(record_type=TRX_TYPE_UNPUBLISH)
            assert_that(record, is_not(none()))
