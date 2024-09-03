from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)
    return updated.urlencode()


@register.simple_tag
def pagination_range(page_obj, boundaries=2, around=1):
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages

    start = list(range(1, min(boundaries + 1, total_pages + 1)))
    middle = list(range(max(current_page - around, 1), min(current_page + around + 1, total_pages + 1)))
    end = list(range(max(total_pages - boundaries + 1, 1), total_pages + 1))
    all_pages = sorted(set(start + middle + end))
    result_list = []

    for index, page in enumerate(all_pages):
        if index > 0 and page != all_pages[index - 1] + 1:
            result_list.append("...")
        result_list.append(page)

    return result_list


