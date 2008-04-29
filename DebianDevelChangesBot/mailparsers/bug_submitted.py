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

from DebianDevelChangesBot import MailParser
from DebianDevelChangesBot.messages import BugSubmittedMessage
from DebianDevelChangesBot.utils import tidy_bug_title, format_email_address

import re

SUBJECT = re.compile(r'^Bug#(\d+): (.+)$')

BTS = re.compile(r'^# Automatically generated email from bts')
FOLLOWUP_FOR = re.compile(r'(?i)^Followup-For:? .+')
PACKAGE = re.compile(r'(?i)^Package:? ([^\s]{1,40})$')
VERSION = re.compile(r'(?i)^Version:? ([^\s]{1,20})$')
SEVERITY = re.compile(r'(?i)^Severity:? (critical|grave|serious|important|normal|minor|wishlist)$')

class BugSubmittedParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') != '<debian-bugs-dist.lists.debian.org>':
            return

        msg = BugSubmittedMessage()

        m = SUBJECT.match(headers['Subject'])
        if m:
            msg.bug_number = int(m.group(1))
            msg.title = m.group(2)
        else:
            return

        msg.by = format_email_address(headers['From'])

        mapping = {
            PACKAGE: 'package',
            VERSION: 'version',
            SEVERITY: 'severity',
        }

        for line in body[:10]:
            if BTS.match(line) or FOLLOWUP_FOR.match(line):
                return

            for command in ('thanks', 'kthxbye'):
                if line.startswith(command):
                    return

            for command in ('retitle', 'reassign'):
                if line.startswith('%s %d' % (command, msg.bug_number)):
                    return

            for pattern, target in mapping.iteritems():
                m = pattern.match(line)
                if m:
                    val = m.group(1).lower()
                    setattr(msg, target, val)
                    del mapping[pattern]
                    break

            if len(mapping.keys()) == 0:
                break

        if type(msg.version) is str and msg.version.find('GnuPG') != -1:
            msg.version = None

        if not msg.package:
            return

        msg.title = tidy_bug_title(msg.title, msg.package)

        return msg
