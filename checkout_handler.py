import requests
import re


def sale_transaction_options(cart_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Access-Control-Request-Method': 'PUT',
        'Access-Control-Request-Headers': 'content-type,x-csrftoken',
        'Referer': 'https://chelseafc.3ddigitalvenue.com/',
        'Origin': 'https://chelseafc.3ddigitalvenue.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    return requests.options(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/sale_transaction/' + str(cart_id),
        headers=headers)


def get_session_string(session_id_cookie):
    match = re.search("sessionid=([a-z0-9]+);", session_id_cookie)
    if match:
        return match.group(1)
    else:
        return session_id_cookie


def sale_transaction_put(cart_id, session_id, csrf, login_response):
    sale_transaction_options_response = sale_transaction_options(cart_id)

    if sale_transaction_options_response.status_code == 200:
        import requests

        cookies = {
            'sessionid': get_session_string(session_id),
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-CSRFTOKEN': csrf,
            'Content-Type': 'application/json',
            'Origin': 'https://chelseafc.3ddigitalvenue.com',
            'Connection': 'keep-alive',
            'Referer': 'https://chelseafc.3ddigitalvenue.com/',
            'Cookie': 'sessionid=' + get_session_string(session_id),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }

        json_data = {
            'delivery_method_id': 1041,
            'delivery_method_type': 'EXTERNAL_TICKETS_AT_HOME',
            'delivery_first_name': login_response[0]["tdc_info"]["first_name"],
            'delivery_last_name': login_response[0]["tdc_info"]["last_name"],
            'delivery_email': login_response[0]["email"],
        }

        return requests.put(
            'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/sale_transaction/' + str(cart_id) + '/',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )


def post_checkout(session_id, stand_id, event_id, customer_ids, stand_data, headers):
    cookies = {
        'sessionid': session_id,
    }

    json_data = {
        'event': event_id,
        'price_scale': stand_id,
        'friends_family_accounts': create_friends_family_accounts(customer_ids, stand_data),
    }

    response = requests.post(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/sale_transaction/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    return response


def create_friends_family_accounts(customer_ids, stand_data):
    friends_family_accounts = []
    for customerId in customer_ids:
        friends_family_account = {"customer": customerId, "seats": create_adult_seats(stand_data)}
        friends_family_accounts.append(friends_family_account)
    return friends_family_accounts


def create_adult_seats(stand_data):
    prices = stand_data.get("prices")
    return {
        str(prices["ADULT"]["id"]): {
            "num_tickets": 1,
            "code": prices["ADULT"]["code"],
            "name": prices["ADULT"]["name"],
        }
    }
