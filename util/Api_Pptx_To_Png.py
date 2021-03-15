from __future__ import print_function

import time
import cloudmersive_convert_api_client
from cloudmersive_convert_api_client.rest import ApiException

def Pptx_To_Png(pptx_input):
    # Configure API key authorization: Apikey
    configuration = cloudmersive_convert_api_client.Configuration()
    configuration.api_key['Apikey'] = 'f0a69dc5-3973-4ab9-9ce8-6a28eda5f67a'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['Apikey'] = 'Bearer'

    # create an instance of the API class
    api_instance = cloudmersive_convert_api_client.ConvertDocumentApi(cloudmersive_convert_api_client.ApiClient(configuration))
    input_file = pptx_input # file | Input file to perform the operation on.

    try:
        # Convert PowerPoint PPTX to PNG image array
        api_response = api_instance.convert_document_pptx_to_png(input_file)
        url = api_response.png_result_pages[0].url

        return url

    except ApiException as e:
        print("Exception when calling ConvertDocumentApi->convert_document_pptx_to_png: %s\n" % e)