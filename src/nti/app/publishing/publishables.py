#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: publishables.py 121423 2017-09-09 22:59:29Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.dataserver.contenttypes.forums.interfaces import IDFLBoard
from nti.dataserver.contenttypes.forums.interfaces import IPersonalBlog
from nti.dataserver.contenttypes.forums.interfaces import ICommunityBoard

from nti.dataserver.interfaces import IUser
from nti.dataserver.interfaces import ICommunity
from nti.dataserver.interfaces import IDataserver
from nti.dataserver.interfaces import IShardLayout
from nti.dataserver.interfaces import IDynamicSharingTargetFriendsList

from nti.publishing.interfaces import IPublishable
from nti.publishing.interfaces import IPublishables

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IPublishables)
class EntityPublishables(object):

    __slots__ = ()

    def __init__(self, *args):
        pass

    def _process_board(self, board, result):
        if not board:
            return result
        for forum in board.values():
            for topic in forum.values():
                if IPublishable.providedBy(topic):
                    result.append(topic)
        return result

    def _all_entities(self):
        dataserver = component.getUtility(IDataserver)
        users_folder = IShardLayout(dataserver).users_folder
        return users_folder.values()

    def iter_objects(self):
        result = []
        for entity in self._all_entities():
            if ICommunity.providedBy(entity):
                self._process_board(ICommunityBoard(entity, None), result)
            elif IUser.providedBy(entity):
                self._process_board(IPersonalBlog(entity, None), result)
                # dfl forums
                for fl in entity.dynamic_memberships:
                    if IDynamicSharingTargetFriendsList.providedBy(fl):
                        self._process_board(IDFLBoard(entity, None),
                                            result)
        return result
