# This file is part of Indico.
# Copyright (C) 2002 - 2016 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from flask import session

from indico.core import signals
from indico.core.logger import Logger
from indico.core.roles import ManagementRole
from indico.modules.events.features.base import EventFeature
from indico.modules.events.models.events import EventType, Event
from indico.util.i18n import _
from indico.web.flask.util import url_for
from indico.web.menu import SideMenuItem


logger = Logger.get('events.abstracts')


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    if not event.can_manage(session.user):
        return
    if event.has_feature('abstracts'):
        return SideMenuItem('abstracts', _('Abstracts'), url_for('abstracts.manage_abstracts', event),
                            section='organization')


@signals.event.get_feature_definitions.connect
def _get_feature_definitions(sender, **kwargs):
    return AbstractsFeature


class AbstractsFeature(EventFeature):
    name = 'abstracts'
    friendly_name = _('Abstracts')
    description = _('Gives event managers the opportunity to open a "Call for Abstracts" and use the abstract '
                    'reviewing workflow.')

    @classmethod
    def is_allowed_for_event(cls, event):
        return event.type_ == EventType.conference

    @classmethod
    def is_default_for_event(cls, event):
        return event.type_ == EventType.conference


@signals.acl.get_management_roles.connect_via(Event)
def _get_management_roles(sender, **kwargs):
    return AbstractReviewerRole


class AbstractReviewerRole(ManagementRole):
    name = 'abstract_reviewer'
    friendly_name = _('Reviewer')
    description = _('Grants abstract reviewing rights on an event.')