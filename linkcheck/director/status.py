# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2008 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""Status message handling"""
import time
from .. import strformat
from . import task


class Status (task.CheckedTask):
    """Status thread."""

    def __init__ (self, urlqueue, logger):
        """Store urlqueue object."""
        super(Status, self).__init__()
        self.urlqueue = urlqueue
        self.logger = logger

    def run_checked (self):
        """Print periodic status messages."""
        self.start_time = time.time()
        self.setName("Status")
        waitfor = range(5)
        while True:
            for dummy in waitfor:
                time.sleep(1)
                if self.stopped():
                    return
            self.print_status()

    def print_status (self):
        """Print a status message."""
        duration = time.time() - self.start_time
        checked, in_progress, queue = self.urlqueue.status()
        msg = _n("%2d URL active", "%2d URLs active", in_progress) % \
          in_progress
        self.logger.write(u"%s, " % msg)
        msg = _n("%5d URL queued", "%5d URLs queued", queue) % queue
        self.logger.write(u"%s, " % msg)
        msg = _n("%4d URL checked", "%4d URLs checked", checked) % checked
        self.logger.write(u"%s, " % msg)
        msg = _("runtime %s") % strformat.strduration_long(duration)
        self.logger.writeln(msg)
        self.logger.flush()
