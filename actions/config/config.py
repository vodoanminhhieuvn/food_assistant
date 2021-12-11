# Load environment variables
# needs to happen before anything else (to properly instantiate constants)

import os

edamam_url_endpoint = "https://api.edamam.com/api/recipes/v2"
edamam_app_id = os.environ.get("EDAMAM_APP_ID", "d736f71a")
edamam_app_key = "5a61563f39257241ba253b7e87328f5a"

ingredient_data_path = "src/actions/api/data"
