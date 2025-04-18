import requests
import hashlib
import time
import os
import urllib.parse

API_URL = "https://api-sg.aliexpress.com/sync" # Or the appropriate endpoint for your region/API version
APP_KEY = os.environ.get("ALIEXPRESS_APPKEY")
APP_SECRET = os.environ.get("ALIEXPRESS_APP_SECRET")
TRACKING_ID = os.environ.get("ALIEXPRESS_TRACKING_ID")

def _sign_request(params):
    # 1. Sort parameters alphabetically
    sorted_params = sorted(params.items())
    # 2. Concatenate key-value pairs
    query_string = "".join([f"{k}{v}" for k, v in sorted_params])
    # 3. Prepend and append app_secret
    string_to_sign = APP_SECRET + query_string + APP_SECRET
    # 4. Calculate MD5 hash and uppercase
    signature = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest().upper()
    return signature

def generate_affiliate_link(original_url):
    if not APP_KEY or not APP_SECRET or not TRACKING_ID:
        print("Error: AliExpress API credentials not set.")
        return None

    params = {
        'app_key': APP_KEY,
        'method': 'aliexpress.affiliate.link.generate',
        'sign_method': 'md5',
        'timestamp': str(int(time.time() * 1000)),
        'format': 'json',
        'tracking_id': TRACKING_ID,
        'source_values': original_url, # API expects comma-separated if multiple, but send one here
        # Add other required params based on documentation (e.g., v, simplify)
    }

    params['sign'] = _sign_request(params)

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()

        # --- Important: Parse the actual response structure ---
        # The structure below is a GUESS based on common API patterns.
        # You MUST check the real AliExpress API documentation for the correct path.
        # Example: data['aliexpress_affiliate_link_generate_response']['resp_result']['result']['promotion_links']['promotion_link'][0]['promotion_link']

        # Simplified hypothetical path - REPLACE with actual path from docs
        result_key = 'aliexpress_affiliate_link_generate_response'
        if result_key in data and 'resp_result' in data[result_key] and 'result' in data[result_key]['resp_result']:
             links_data = data[result_key]['resp_result']['result']
             if 'promotion_links' in links_data and 'promotion_link' in links_data['promotion_links'] and len(links_data['promotion_links']['promotion_link']) > 0:
                 # Assuming the first link is the one we want
                 aff_link = links_data['promotion_links']['promotion_link'][0].get('promotion_link')
                 # Optionally get price/title if available in this response, or make another call
                 return aff_link
        else:
             print(f"Error generating link. Response: {data}")
             return None

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except KeyError as e:
         print(f"Error parsing API response: Missing key {e}. Response: {data}")
         return None
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred: {e}")
        return None


# Optional: Add function get_product_details(product_url_or_id)
# Similar structure: build params, sign, make request, parse response
