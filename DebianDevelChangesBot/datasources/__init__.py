# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import testing_rc_bugs
import new_queue
import rm_queue
import maintainer

state = testing_rc_bugs.TestingRCBugs._shared_state
reload(testing_rc_bugs)
testing_rc_bugs.TestingRCBugs._shared_state = state

state = new_queue.NewQueue._shared_state
reload(new_queue)
new_queue.NewQueue._shared_state = state

state = rm_queue.RmQueue._shared_state
reload(rm_queue)
rm_queue.RmQueue._shared_state = state

state = maintainer.Maintainer._shared_state
reload(maintainer)
maintainer.Maintainer._shared_state = state

from testing_rc_bugs import TestingRCBugs
from new_queue import NewQueue
from rm_queue import RmQueue
from maintainer import Maintainer

def get_datasources():
    for klass in TestingRCBugs, NewQueue, RmQueue:
        yield klass, klass.INTERVAL, klass.__name__
