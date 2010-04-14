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
"""Functional test suite for the media controller"""

import transaction
from nose.tools import assert_true, assert_false, eq_
from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Media, MediaData


class TestMediaController(TestController):
    """Tests for the methods in the media controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        media = Media(u'image', u'http://example.com', tadm, u'xx',
                                                                u'random text')
        DBSession.add(media)
        DBSession.flush()
        languageid = language.id
        mediaid = media.id
        transaction.commit()
        return languageid, mediaid

    def test_get_all(self):
        """controllers.media.Controller.get_all is working properly"""
        languageid, mediaid = self._fill_db()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/media/', extra_environ=environ, status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>%s</td>' % mediaid)
        eq_(str(tr('td')[1]), '<td>image</td>')
        eq_(str(tr('td')[2]), '<td>http://example.com</td>')
        eq_(str(tr('td')[3]), '<td>random text</td>')
        eq_(str(tr('td')[4]), '<td>%s</td>' % languageid)
        actions = tr('td')[5]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_get_one(self):
        """controllers.media.Controller.get_one is working"""
        languageid, mediaid = self._fill_db()

        response = self.app.get('/media/%s' % mediaid)

        expected = ('<div id="content_with_side">\n'
                    '<div>%s</div>\n'
                    '<div>image</div>\n'
                    '<div>http://example.com</div>\n'
                    '<div>random text</div>\n'
                    '</div>' % mediaid
                   )

        eq_(str(response.html.find(id='content_with_side')), expected)

    def test_new(self):
        """controllers.media.Controller.new is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/media/new', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/media/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'id': 'languageid'}),
                                        '"languageid" input element not found')
        assert_true(response.html.find('select', {'id': 'mediatype'}),
                                    '"mediatype" input element not found')
        assert_true(response.html.find('input', {'id': 'uri'}),
                                    '"uri" input element not found')
        assert_true(response.html.find('textarea', {'id': 'description'}),
                                    '"description" textarea element not found')

    def test_post(self):
        """controllers.media.Controller.post is working properly"""
        languageid, mediaid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/media/', dict(mediatype='image',
                                                 uri='http://example.com',
                                                 languageid=languageid,
                                                 description='random text',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        query = DBSession().query(Media)
        media = query.filter_by(uri=u'http://example.com').first()
        eq_(media.type, u'image')
        eq_(media.description[''], u'random text')
        eq_(media.language_ids, set([languageid]))
        eq_(media.user.user_name, 'test_admin')

    def test_edit(self):
        """controllers.media.Controller.edit is working"""
        languageid, mediaid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/media/%s/edit' % mediaid,
                                            extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/media/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                        {'name': '_method', 'value': 'PUT'}),
                                        '"_method" should be "PUT"')
        assert_true(response.html.find('input',
                                {'name': 'mediaid', 'value': str(mediaid)}),
                                'wrong media_id')
        elem_mediatype = response.html.find('select', {'id': 'mediatype'})
        assert_true(elem_mediatype, '"mediatype" input element not found')
        elem_languageid = response.html.find('select', {'id': 'languageid'})
        assert_true(elem_languageid, '"languageid" input element not found')
        eq_(elem_languageid.find('option', {'selected': 'selected'})['value'],
                                                            languageid)
        eq_(response.html.find('input', {'id': 'uri'})['value'],
                                                        u'http://example.com')
        eq_(response.html.find('textarea', {'id': 'description'}).string,
                                                        u'random text')

    def test_put(self):
        """controllers.media.Controller.put is working properly"""
        languageid, mediaid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.put('/media/%s' % mediaid,
                                            dict(mediatype='video',
                                                 uri='changed',
                                                 languageid=languageid,
                                                 description='Changed',
                                                ),
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        media = DBSession.query(Media).get(mediaid)
        eq_(media.type, 'video')
        eq_(media.uri, 'changed')
        eq_(media.description[languageid], 'Changed')

    def test_get_delete(self):
        """controllers.media.Controller.get_delete is working properly"""
        languageid, mediaid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/media/%s/delete' % mediaid,
                                           extra_environ=environ, status=200)

        eq_(response.html.form['action'], u'/media/')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('input',
                                {'name': '_method', 'value': 'DELETE'}),
                                '"_method" should be "DELETE"')
        assert_true(response.html.find('input',
                                {'name': 'mediaid', 'value': str(mediaid)}),
                                'wrong media_id')

    def test_post_delete(self):
        """controllers.media.Controller.post_delete is working properly"""
        languageid, mediaid = self._fill_db()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.delete('/media?mediaid=%s' % mediaid,
                                            extra_environ=environ, status=302)
        redirected = response.follow(extra_environ=environ, status=200)

        assert_true(redirected.html.find(id='flash').find('div', 'ok'),
                                'result should have a "ok" flash notification')

        media = DBSession.query(Media).get(mediaid)
        assert_true(media is None,
                            'Media "1" should have been deleted from the db')
        mediadata = DBSession.query(MediaData).filter_by(parent_id=None).all()
        assert_false(mediadata,
                    'orphaned MediaData should have been deleted from the db')

    def test_translation(self):
        """controllers.media.Controller.translation is working properly"""
        languageid, mediaid = self._fill_db()

        response = self.app.post('/media/', dict(mediaid=mediaid,
                                               value=languageid,
                                               _method='TRANSLATION',
                                              )
                                )

        expected = '{"description": "random text"}'
        eq_(response.body, expected)

