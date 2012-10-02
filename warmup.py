# -*- coding: utf-8 -*-
# Copyright (C) 2012 Sergio Gabriel Teves
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from google.appengine.ext import webapp 
from google.appengine.ext.webapp.util import run_wsgi_app

class WarmUp(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write("OK")

def main():
    application = webapp.WSGIApplication(
                                     [
                                     ('/warmup',WarmUp)
                                     ])  
    run_wsgi_app(application)
  
if __name__ == "__main__":
    main()