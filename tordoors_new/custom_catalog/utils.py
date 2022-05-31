def get_model_field(object, attr):
    """ Поиск атрибута модели по дереву каталога """
    try:
        self_attr = getattr(object, attr)
    except:
        self_attr = ''
    if self_attr:
        return self_attr
    else:
        try:
            return get_model_field(object.tree.get().parent.content_object, attr)
        except:
            return ''
    return ''