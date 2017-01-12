from flask import Blueprint, redirect, request, current_app

from ..domain import Text

from ._utils import route


blueprint = Blueprint('magic', __name__, url_prefix="/api/magic/")


@blueprint.route("<pattern>")
@blueprint.route("", defaults={'pattern': None}, endpoint='get')
def links(pattern):
    """Get a list of all matching links."""
    if not pattern:
        return []

    text = Text(pattern)

    if text.path != pattern:
        return redirect(route('.links', pattern=text.path))

    return _get_matches(str(text).lower())


def _get_matches(pattern):
    items = []

    for template in current_app.template_service.all():
        ratio, path = template.match(pattern)
        if not ratio:
            continue

        data = {}
        data['ratio'] = ratio
        data['link'] = route('links.get', key=template.key,
                             path=path, _external=True)

        items.append(data)

    return sorted(items, key=lambda item: item['ratio'], reverse=True)


@blueprint.route("<pattern>.jpg")
def image(pattern):
    """Get the first matching image."""
    # TODO: share this logic
    text = Text(pattern)

    items = []

    for template in current_app.template_service.all():
        ratio, path = template.match(str(text).lower())
        if not ratio:
            continue

        data = {}
        data['ratio'] = ratio
        data['image'] = route('image.get',
                              key=template.key, path=path, **request.args)

        items.append(data)

    try:
        url = max(items, key=lambda item: item['ratio'])['image']
    except ValueError:
        url = route('image.get', key="unknown", path="_")

    return redirect(url)
