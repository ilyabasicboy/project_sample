# -*- coding: utf-8 -*-
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, 'ei60doors')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
FILE_UPLOAD_PERMISSIONS = 0o644  # права для записи файлов, размером > FILE_UPLOAD_MAX_MEMORY_SIZE

APPEND_SLASH = True
DEBUG = True
SITE_ID = 2
SECRET_KEY = ''
WSGI_APPLICATION = 'ei60doors.wsgi.application'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'ei60doors.urls'
LANGUAGE_CODE = 'ru'

MANAGERS = ADMINS = [
    ('websupport', 'websupport+ei60doors@redsolution.ru'),
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[ei60doors]'
DEFAULT_FROM_EMAIL = 'no-reply@ei60doors.ru'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'import_redirects',
    'adminsortable2',
    'mptt',
    'dj_pagination',
    'ei60doors',
    'ei60doors.service',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'ei60doors.save_referer.middleware.RequestCookies',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'ei60doors',
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 2,
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ei60doors',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# ~========== ADMIN REORDER ===========~
INSTALLED_APPS += ['admin_reorder', ]
MIDDLEWARE += ['ei60doors.middleware.CustomModelAdminReorder']
ADMIN_REORDER = (
    {
        'app': 'pages', 'label': u'Контент сайта',
        'models': (
            'pages.Page', 'catalog.TreeItem', 'chunks.Chunk', 'treemenus.Menu', 'filebrowser.FileBrowser',
            'custom_pages.Advantage'
        )
    },
    {
        'app': 'catalog', 'label': u'Каталог сайта',
        'models': (
            'catalog.TreeItem', 'custom_catalog.Section', 'custom_catalog.Category',
            'custom_catalog.Product', 'custom_catalog.Root',
        )
    },
    {
        'app': 'feedback', 'label': u'Обратная связь',
    },
    {
        'app': 'seo', 'label': u'Seo',
        'models': (
            'seo.Url', 'redirects.Redirect', 'redirects.ImportModel'
        )
    }
)

# ~========== FILEBROWSER ===========~
INSTALLED_APPS = ['filebrowser'] + INSTALLED_APPS
FILEBROWSER_DIRECTORY = 'upload/attachment/source/'
FILEBROWSER_VERSIONS_BASEDIR = 'upload/attachment/cache/upload/attachment/source/'
FILEBROWSER_OVERWRITE_EXISTING = False
FILEBROWSER_CONVERT_FILENAME = False
FILEBROWSER_MAX_UPLOAD_SIZE = 20485760
FILEBROWSER_VERSION_QUALITY = 90
FILEBROWSER_VERSION_NAMER = 'ei60doors.custom_attachment.namers.VersionNamer'
FILEBROWSER_VERSION_PROCESSORS = ['ei60doors.custom_attachment.processors.filebrowser_processor']
FILEBROWSER_ADMIN_THUMBNAIL = 'Thumb'
FILEBROWSER_ADMIN_VERSIONS = ['Thumb300', 'Thumb500', 'Display']
FILEBROWSER_VERSIONS = {
    'Thumb': {'verbose_name': 'Thumb'},
    'Thumb300': {'verbose_name': 'Thumb300'},
    'Thumb500': {'verbose_name': 'Thumb500'},
    'Display': {'verbose_name': 'Display'},
}

FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Document': ['.pdf','.doc', '.docx','.rtf','.txt','.xls','.xlsx','.csv','.svg','.zip','.rar', ],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
}

# ~========== DJANGO PAGES CMS ===========~
INSTALLED_APPS += ['pages', 'ei60doors.custom_pages']
PAGE_DEFAULT_TEMPLATE = 'pages/default.html'
PAGE_USE_STRICT_URL = True
PAGE_HIDE_ROOT_SLUG = True
PAGE_USE_LANGUAGE_PREFIX = False
PAGE_LANGUAGES = (('ru', 'Russian'),)
TEMPLATES[0]['OPTIONS']['context_processors'].append('pages.context_processors.media')

PAGE_TEMPLATES = (
    ('pages/frontpage.html', u'Главная страница'),
    ('pages/default.html',   u'Шаблон по умолчанию'),
    ('pages/list.html',      u'Список'),
    ('pages/contacts.html',  u'Контакты'),
    ('pages/finish.html',  u'Страница отделки'),
    ('pages/gallery.html',  u'Галерея'),
    ('pages/slide.html',  u'Слайд'),
)

# ~======== DJANGO TINYMCE ========~
INSTALLED_APPS += ['tinymce']
PAGE_TINYMCE = True
TINYMCE_DEFAULT_CONFIG = {
    'mode': 'exact',
    'theme': 'advanced',
    'relative_urls': False,
    'width': 1024,
    'height': 300,
    # 'content_css': '%scss/tinymce.css' % STATIC_URL,
    'skin': 'o2k7',
    'plugins': 'table,advimage,advlink,inlinepopups,preview,media,searchreplace,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras',
    'theme_advanced_buttons1': 'justifyleft,justifycenter,justifyright,|,bold,italic,underline,strikethrough,|,sub,sup,|,bullist,numlist,|,outdent,indent,|,formatselect,removeformat,cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,link,unlink,anchor,image,media,charmap,|,visualchars,nonbreaking',
    'theme_advanced_buttons2': 'visualaid,tablecontrols,|,blockquote,del,ins,|preview,fullscreen,|,code',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'valid_elements': '*[*]',
    'extended_valid_elements': '*[*]',
    'custom_elements': 'noindex',
    'external_image_list_url': 'images/',
    'external_link_list_url': 'links/',
    'paste_remove_styles': 'true',
    'paste_remove_styles_if_webkit': 'true',
    'paste_strip_class_attributes': 'all',
    'plugin_preview_width': '900',
    'plugin_preview_height': '800',
    'accessibility_warnings': 'false',
    'theme_advanced_resizing': 'true',
    'content_style': '.mcecontentbody{font-size:14px;}',
}

# ~======== CAPTCHA ===============~
INSTALLED_APPS += ['nocaptcha_recaptcha']
NORECAPTCHA_SITE_KEY = ''
NORECAPTCHA_SECRET_KEY = ''

# ~======== FEEDBACK ==============~
INSTALLED_APPS += ['feedback', 'ei60doors.custom_feedback']
FEEDBACK_PREFIX_KEY_FIELDS = True
FEEDBACK_ADMIN_EXTRA_CLASS = {'all': 'large-input'}
FEEDBACK_ADMIN_EXTRA_CSS = {'all': ['css/admin/common.css']}
FEEDBACK_FORMS = {
    'metering_call': 'ei60doors.custom_feedback.forms.MeteringCall',
    'feedback_call': 'ei60doors.custom_feedback.forms.FeedbackCall',
    'order': 'ei60doors.custom_feedback.forms.Order',
    'call_rackman': 'ei60doors.custom_feedback.forms.CallRackman',
    'want_similar': 'ei60doors.custom_feedback.forms.WantSimilar',
    'consult': 'ei60doors.custom_feedback.forms.Consult',
}

FEEDBACK_FORMS_NAMES = {
    'metering_call': u'Запросить расчет',
    'feedback_call': u'Обратный звонок',
    'order': u'Оформить предзаказ',
    'call_rackman': u'Вызвать замерщика',
    'want_similar': u'Интересует похожее изделие',
    'consult': u'Получить консультацию',
}

# ~======== CHUNKS =================~
INSTALLED_APPS += ['chunks']
TEMPLATES[0]['OPTIONS']['context_processors'] += ['chunks.context_processors.chunks_processor']

# ~======== TREEMENUS ==============~
INSTALLED_APPS += ['treemenus']
TREEMENUS_NAMES = {
    'main_menu':  u'Главное меню',
    'main_menu_modal':  u'Главное меню в модальном окне',
    'add_menu':  u'Доп. меню',
}

# ~======== CATALOG ================~

INSTALLED_APPS += ['catalog', 'ei60doors.custom_catalog']

CATALOG_MODELS = [
    'custom_catalog.Section',
    'custom_catalog.Product',
    'custom_catalog.Category',
    'custom_catalog.Root',
]

CATALOG_SITEMAP_HTML_MODELS = ['Section', 'Category']

# ~======== ATTACHMENTS ============~

INSTALLED_APPS += [
    'unidecode',
    'imagekit',
    'attachment',
    'ei60doors.custom_attachment',
]
ATTACHMENT_EXTRA_IMAGES = 0
ATTACHMENT_EXTRA_FILES = 0
ATTACHMENT_IKSPECS = 'ei60doors.custom_attachment.ikspecs'
ROLE_GALLERY = u'галерея'
ROLE_ADD_IMAGE = u'доп. фото'
ATTACHMENT_IMAGE_ROLES = [ROLE_GALLERY, ROLE_ADD_IMAGE]
# ATTACHMENT_SPECS_FOR_TINYMCE = ['displaywatermark']
ATTACHMENT_FOR_MODELS = [
    'pages.Page',
    'service.ErrorPage',
    'custom_catalog.Root',
    'custom_catalog.Section',
    'custom_catalog.Category',
    'custom_catalog.Product',
]
ATTACHMENT_LINK_MODELS = [
    'pages.Page',
    'service.ErrorPage',
    'custom_catalog.Root',
    'custom_catalog.Section',
    'custom_catalog.Product',
]

# ~======== SEO =================~
INSTALLED_APPS += ['seo']
SEO_FOR_MODELS = [
    'pages.Page',
    'service.ErrorPage',
    'custom_catalog.Product',
    'custom_catalog.Section',
    'custom_catalog.Category',
    'custom_catalog.Root',
]
