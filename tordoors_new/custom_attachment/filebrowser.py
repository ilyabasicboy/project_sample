from . import ikspecs


def filebrowser_processor(img, verbose_name):

    """ Применение файлбраузером процессоров из attachments """

    ResizeClass = getattr(ikspecs, verbose_name)
    img, fmt = ResizeClass.process(img, None)
    return img