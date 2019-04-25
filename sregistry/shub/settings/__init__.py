from importlib import import_module

from .applications import *
from .config import *
from .main import *
from .logging import *
from .auth import *
from .api import *
from .tasks import *

# If PAM_AUTH in plugins enbled, add django_pam
if "pam_auth" in INSTALLED_APPS:
    INSTALLED_APPS += ['django_pam']

# Apply any plugin settings
for plugin in PLUGINS_ENABLED:

    plugin_module = 'shub.plugins.' + plugin
    plugin = import_module(plugin_module)

    # Add the plugin to INSTALLED APPS
    INSTALLED_APPS.append(plugin_module)

    # Add AUTHENTICATION_BACKENDS if defined, for authentication plugins
    if hasattr(plugin, 'AUTHENTICATION_BACKENDS'):
        AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + plugin.AUTHENTICATION_BACKENDS

    # Add custom context processors, if defines for plugin
    if hasattr(plugin, 'CONTEXT_PROCESSORS'):
        for context_processor in plugin.CONTEXT_PROCESSORS:
            TEMPLATES[0]['OPTIONS']['context_processors'].append(context_processor)
