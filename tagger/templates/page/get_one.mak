<%inherit file="local:templates.master"/>
<%namespace name="sidebars" file="local:templates.sidebars"/>

<%!
    from tagger.lib.render.rst import render_text
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Article')
%>

${c.w_object_title(obj=article, tg=tg, lang=lang) | n}

<div>
    ${render_text(page.text[lang], lang) | n}
</div>

<%def name="side()">
    ${sidebars.side_related()}
</%def>

