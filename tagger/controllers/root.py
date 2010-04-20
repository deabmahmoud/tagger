# -*- coding: utf-8 -*-
#
# This file is part of Tagger.
#
# Tagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect, response
from tg import tmpl_context
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
from tg.exceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

from tagger.lib.base import BaseController
from tagger.lib.widgets import FormLogin
from tagger.controllers.error import ErrorController
from tagger.controllers import admin, language, category, article, link, media
from tagger.controllers import tag, comment
from tagger.model import DBSession, Language, Category, Article

__all__ = ['RootController']

f_login = FormLogin(action=url('/login_handler'))


class RootController(BaseController):
    """The root controller for the tagger application."""
    admin = admin.Controller()
    error = ErrorController()
    category = category.Controller()
    language = language.Controller()
    article = article.Controller()
    link = link.Controller()
    media = media.Controller()
    tag = tag.Controller()
    comment = comment.Controller()

    @expose('tagger.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('tagger.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        tmpl_context.f_login = f_login

        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        fargs = dict(came_from=came_from, logins=str(login_counter))
        return dict(page='login', fargs=fargs)

    @expose()
    def post_login(self, came_from='/'):
        """Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.
        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash('%s, %s!' % (_('Welcome back'), userid))
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """Redirect the user to the root page on logout and say
        goodbye as well."""
        flash(_('We hope to see you soon!'))
        redirect('/')

    @expose()
    def set_language(self, languageid, came_from=url('/')):
        """Set language cookie"""
        language = DBSession.query(Language).get(languageid.decode())
        response.set_cookie('lang', language.id)
        flash('%s %s' % (_('Preferred language set to:'), language.name))
        redirect(came_from)

    @expose()
    def unset_language(self, came_from=url('/')):
        """Delete language cookie"""
        response.delete_cookie('lang')
        flash(_('No preferred language'))
        redirect(came_from)

    @expose('tagger.templates.article.get_one')
    def _default(self, *args, **kwargs):
        if 'categoryid' in kwargs and 'articleid' in kwargs:
            categoryid = kwargs['categoryid']
            articleid = kwargs['articleid']
        elif len(args) >= 2:
            categoryid = args[0]
            articleid = args[1]
        else:
            raise HTTPNotFound

        if 'languageid' in kwargs:
            languageid = kwargs['languageid']
        elif len(args) >= 3:
            languageid = args[2]
        else:
            languageid = None

        try:
            category = DBSession.query(Category).filter_by(
                                            id=categoryid.decode()).one()
            article = DBSession.query(Article).filter_by(
                    category_id=category.id, id=articleid.decode()).one()
        except NoResultFound:
            raise HTTPNotFound

        return self.article.get_one(article.id, languageid)


