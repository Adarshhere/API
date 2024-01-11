# __all__=["user_controller","product_controller","product_categories_controller"]

import os
import glob

__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
