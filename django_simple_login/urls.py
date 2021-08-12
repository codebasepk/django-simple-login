#
# Copyright (C) CODEBASE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls import include, url
from django.contrib import admin

from sample_app import urls as exp_urls
from simple_login.views import TwitterLoginAPIView, FacebookLoginAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(exp_urls)),
    url(r'^api/twitter/', TwitterLoginAPIView.as_view()),
    url(r'^api/facebook/', FacebookLoginAPIView.as_view())
]
