<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<%!
    from tg.configuration import Bunch
    show_side = True
%>

<html>
<head>
    ${self.meta()}
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/themes/%s/css/style.css' % c.theme)}" />

    ##${c.j_startup()}
    <script type="text/javascript">
    $(function() {
        % if page:
            % if page[0]:
                $("#header .menu_bottom .${page[0]}").addClass('active');
            % endif
            % if page[1]:
                $("#side .${page[1]}").addClass('active');
            % endif
        % endif
    });
    </script>
</head>

<body>
    <div id="overlay">
        <div class="wrap"></div>
        <iframe src="about:blank"></iframe>
    </div>

    ${self.header()}

    <div id="main">
        % if self.attr.show_side:
            <div id="side">
                ${self.side()}
            </div>
        % endif
        ${self.content_wrapper()}
    </div>
    ${self.footer()}
</body>

<%def name="content_wrapper()">
    % if self.attr.show_side:
        <div id="content_with_side">
            ${self.body()}
        </div>
    % else:
        <div id="content_without_side">
            ${self.body()}
        </div>
    % endif
</%def>

<%def name="meta()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()">
    ${c.title}
</%def>

<%def name="header()">
    <script type="text/javascript">
        $(function() {
            $(".menu_top .languages").addClass("hidden");
            $(".menu_top .language_chooser").click(
                function(event){$(".menu_top .languages").toggle("fast");}
            ).hover(
                function(event){},
                function(event){$(".menu_top .languages").hide("fast");}
            );
        });
    </script>
    <div id="header">
        <div class="logo"></div>
        <div class="menu_top">
            <ul>
                <li class="language_chooser">
                    <div class="current_language">${c.lang and '%s: %s' % (_('preferred language'), c.lang) or _('choose a language')}</div>
                    <div class="languages">
                        % for language in [l for l in c.languages if l.id != c.lang]:
                            <div class="language"><a href="${tg.url('/set_language/%s?came_from=%s' % (language.id, c.current_url))}">${language.name}</a></div>
                        % endfor
                        % if c.lang:
                            <div class="language"><a href="${tg.url('/unset_language/?came_from=%s' % c.current_url)}">${_('(none)')}</a></div>
                        % endif
                    </div>
                </li>
                <li class="authbox">
                    % if request.identity is None:
                        <a class="login" href="${tg.url('/login')}">login</a>
                    % else:
                        <a class="logout" href="${tg.url('/logout_handler')}">logout ${c.user.user_name}</a>
                    % endif
                </li>
            </ul>
        </div>
        <div class="banner">
            <%
                extra=Bunch(lang=c.lang, url=tg.url)
                if c.banner_mediaid:
                    banner_content = c.w_media(mediaid=c.banner_mediaid, width=1065, height=120, extra=extra)
                else:
                    banner_content = ' '
                if c.banner_linkid:
                    banner_content = c.w_link(linkid='example', label=banner_content, extra=extra)
            %>
            ${banner_content | n}
        </div>
        ${self.flash_wrapper()}
        <div class="menu_bottom">
            <ul>
                <li class="home"><a href="${tg.url('/')}">${_('home')}</a></li>
                % for cat in c.categories:
                <li class="${cat.name[c.lang]}"><a href="${tg.url('/%s/' % cat.name[c.lang])}">${cat.name[c.lang]}</a></li>
                % endfor
                <li class="media"><a href="${tg.url('/media')}">${_('media')}</a></li>
                <li class="links"><a href="${tg.url('/link')}">${_('links')}</a></li>
                % if tg.predicates.has_permission('manage'):
                <li class="admin"><a href="${tg.url('/admin')}">${_('admin')}</a></li>
                % endif
            </ul>
        </div>
    </div>
</%def>

<%def name="flash_wrapper()">
    <%
    flash = tg.flash_obj.render('flash', use_js=False)
    %>
    % if flash:
        ${flash | n}
    % endif
</%def>

<%def name="side()">
</%def>

<%def name="side_related()">
    <ul>
        % for obj, numtags, created in related:
            <li class="related ${obj.type}"><a href="">${obj}</a></li>
        % endfor
    </ul>
</%def>

<%def name="footer()">
    <div id="footer">
        <div class="copyright">${c.copyright}</div>
    </div>
</%def>

</html>
