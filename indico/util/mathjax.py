# This file is part of Indico.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
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

from __future__ import absolute_import

from indico.legacy.common.TemplateExec import render


class MathjaxMixin:
    def _getHeadContent(self):
        return (render('js/mathjax.config.js.tpl') +
                b'\n'.join(b'<script src="{0}" type="text/javascript"></script>'.format(url)
                           for url in self._asset_env['mathjax_js'].urls()))
