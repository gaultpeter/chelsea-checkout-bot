import requests


def ipg_online_payment_processing(purchase_response):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '680',
        'Origin': 'https://chelseafc.3ddigitalvenue.com',
        'Connection': 'keep-alive',
        'Referer': 'https://chelseafc.3ddigitalvenue.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1'
    }

    data = {
        'txntype': purchase_response["txntype"],
        'timezone': purchase_response["timezone"],
        'txndatetime': purchase_response["txndatetime"],
        'hash_algorithm': 'SHA256',
        'hash': purchase_response["hashExtended"],
        'storename': purchase_response["storename"],
        'chargetotal': purchase_response["amount"],
        'currency': purchase_response["currency"],
        'oid': purchase_response["oid"],
        'customParam_transaction': str(purchase_response["id"]),
        'responseSuccessURL': purchase_response["responseSuccessURL"],
        'responseFailURL': purchase_response["responseFailURL"],
        'transactionNotificationURL': purchase_response["transactionNotificationURL"],
        'checkoutoption': 'combinedpage'
    }

    return requests.post('https://www.ipg-online.com/connect/gateway/processing', headers=headers, data=data)
