<%inherit file="local:templates.admin.index"/>

<%!
    from pylons.i18n import lazy_ugettext as l_
    subtitle = l_('Media')
%>

${dummy or ''}

<div class="content_title">
    <h1>${_('Media')}</h1>
    <a class="button overlay" href="${tg.url('/media/new')}" rel="#overlay">${_('add new')}</a>
</div>

<table>
    <tr class="table_header">
        <th>${_('ID')}</th>
        <th>${_('Type')}</th>
        <th>${_('Name')}</th>
        <th>${_('URI')}</th>
        <th>${_('Tags')}</th>
        <th>${_('Languages')}</th>
        <th>${_('Actions')}</th>
    </tr>
    % for m in media:
    <tr>
        <td>${m.id}</td>
        <td>${m.type}</td>
        <td>${m.name[c.lang]}</td>
        <td>${m.uri}</td>
        <td>${', '.join([t.name[lang] for t in m.tags])}</td>
        <td>${', '.join(m.language_ids)}</td>
        <td>
            <a class="icon edit overlay" title="${_('edit')}" href="${tg.url('/media/%s/edit' % m.id)}" rel="#overlay"></a>
            <a class="icon delete overlay" title="${_('delete')}" href="${tg.url('/media/%s/delete' % m.id)}" rel="#overlay"></a>
        </td>
    </tr>
    % endfor
</table>
