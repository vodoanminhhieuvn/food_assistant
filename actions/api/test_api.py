from __future__ import print_function
import time
import spoonacular
from spoonacular.rest import ApiException
from pprint import pprint

configuration = spoonacular.Configuration()
# Configure API key authorization: apiKeyScheme
configuration.api_key["apiKey"] = "630f23d681534cd7b10aaa492800a5cd"
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# create an instance of the API class
api_instance = spoonacular.IngredientsApi(spoonacular.ApiClient(configuration))
query = "burger"  # str | The (natural language) search query. (optional)
number = 10  # int | The maximum number of items to return (between 1 and 100). Defaults to 10. (optional) (default to 10)
meta_information = False  # bool | Whether to return more meta information about the ingredients. (optional)
intolerances = "egg"  # str | A comma-separated list of intolerances. All recipes returned must not contain ingredients that are not suitable for people with the intolerances entered. See a full list of supported intolerances. (optional)

try:
    # Autocomplete Ingredient Search
    api_response = api_instance.autocomplete_ingredient_search(
        query=query,
        number=number,
        meta_information=meta_information,
        intolerances=intolerances,
    )
    pprint(api_response)
except ApiException as e:
    print(
        "Exception when calling IngredientsApi->autocomplete_ingredient_search: %s\n"
        % e
    )
