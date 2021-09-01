from .models import Tag

def all_tag(request):
    tag_list = Tag.objects.all()

    params = {
        'tag_list': tag_list,
    }

    return params