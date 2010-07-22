<%!
    from tg import tmpl_context as c, url
%>

<div>
    <a href="${url('/media/%s' % obj.id)}">
        <h2>${obj.name[c.lang]}</h2>
        <div class="info">
            <span class="icon ${obj.type}"></span>
            <span class="type">${obj.type}</span>
            <span class="date">${obj.created}</span>
            <span class="user">${obj.user.user_name}</span>
        </div>
        <div class="clearing"></div>
        ${c.w_media(mediaid=obj.id, lang=c.lang, width=100)}
    </a>
</div>

