from .mwaah import MWAAH  # noqa
import importlib.metadata

__title__ = "mwaah"
m = importlib.metadata.metadata(__title__)

__description__ = m.get('Summary')
__url__ = m.get('Project-URL')
__version__ = "0.1.1"
__author__ = "Gregory Wiltshire"
__author_email__ = m.get('Author-email')
__license__ = m.get('License')
__copyright__ = "Copyright 2022 Gregory Wiltshire"
__mwaah__="\U0001F618"
