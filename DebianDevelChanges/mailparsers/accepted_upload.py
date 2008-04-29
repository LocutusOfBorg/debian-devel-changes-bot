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

from DebianDevelChanges import MailParser
from DebianDevelChanges.utils import quoted_printable
from DebianDevelChanges.messages import AcceptedUploadMessage

class AcceptedUploadParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') not in ('<debian-devel-changes.lists.debian.org>',
            '"backports.org changes" <backports-changes.lists.backports.org>'):
            return

        msg = AcceptedUploadMessage()

        mapping = {
            'Source': 'package',
            'Version': 'version',
            'Distribution': 'distribution',
            'Urgency': 'urgency',
            'Changed-By': 'by',
            'Closes': 'closes',
        }

        for line in body:
            for field, target in mapping.iteritems():
                if line.startswith('%s: ' % field):
                    val = line[len(field) + 2:]
                    setattr(msg, target, val)
                    del mapping[field]
                    break

            # If we have found all the field, stop looking
            if len(mapping) == 0:
                break

        if msg.by:
            msg.by = quoted_printable(msg.by)

        try:
            if msg.closes:
                msg.closes = [int(x) for x in msg.closes.split(' ')]
        except ValueError:
            return

        return msg
