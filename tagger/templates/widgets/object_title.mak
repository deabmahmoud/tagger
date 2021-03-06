<%!
    from tg import url
    from tagger.model import Article, Media, Link
%>
<%
    if isinstance(obj, Article):
        name = obj.title[lang]
        prefix = '/%s' % obj.category.id
    elif isinstance(obj, Media):
        name = obj.name[lang]
        prefix = '/media'
    elif isinstance(obj, Link):
        name = obj.name[lang]
        prefix = '/link'
    else:
        name = ''
        prefix = ''
%>

<div class="object_title">
    <h1>
        % if add_link:
            <a href="${url('%s/%s' % (prefix, obj.id))}">
        % endif
                ${name}
        % if add_link:
            </a>
        % endif
    </h1>
    <div>
        <span class="date">${obj.created}</span>
        <span class="user">${obj.user.user_name}</span>
    </div>
    <div class="tags">
        % for tag in obj.tags:
            <a class="tag" href="${url('%s?tag=%s' % (prefix, tag.id))}">
                ${tag.name[lang]}
            </a>
        % endfor
    </div>
    <div class="languages">
        % for language in obj.languages:
            <a class="language ${(lang and language.id == lang and 'active') or (not lang and language.id==obj.language_id and 'active') or ''}"
                title="${language.name}"
                href="${url('%s/%s/%s' % (prefix, obj.id, language.id))}"
                >
                    ${language.name}
            </a>
        % endfor
    </div>
</div>

