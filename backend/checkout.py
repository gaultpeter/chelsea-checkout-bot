import json
import threading

from backend.login import get_logged
from backend.seating import get_seating
from backend.checkout_handler import sale_transaction_put, post_checkout
from backend.ipg_online_payment import ipg_online_payment_processing


def start_checkout(session_id, event_id, headers, supporter_numbers, csrf, login_response):
    seating_response = get_seating(event_id, session_id, headers)
    threads = []
    checkout_results = []  # create an empty array to store the checkout results
    for stand_id, stand_data in seating_response.items():
        if stand_data.get("prices").get("ADULT"):
            t = threading.Thread(target=checkout, args=(session_id, event_id, stand_id, supporter_numbers,
                                                        stand_data, headers, csrf, login_response))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
        checkout_result = t.checkout_result  # get the checkout result from the thread
        checkout_results.append(checkout_result)  # append it to the checkout results array
    return checkout_results  # return the checkout results array


def checkout(session_id, event_id, stand_id, supporter_numbers, stand_data, headers, csrf, login_response):
    checkout_response = post_checkout(session_id, stand_id, event_id, supporter_numbers, stand_data, headers)
    if checkout_response.status_code == 201:
        cart_id = json.loads(checkout_response.text)['id']
        sale_transaction_put_response = sale_transaction_put(cart_id, session_id, csrf, login_response)
        if sale_transaction_put_response.status_code == 200:
            sale_transaction_response = json.loads(sale_transaction_put_response.text)
            ipg_online_payment_processing_response = ipg_online_payment_processing(sale_transaction_response)
            threading.current_thread().checkout_result = get_ticket_checkout_info(cart_id,
                                                                                  headers,
                                                                                  ipg_online_payment_processing_response,
                                                                                  session_id)
    else:
        threading.current_thread().checkout_result = "Error: " + json.loads(checkout_response.text)['message']


def get_ticket_checkout_info(cart_id, headers, ipg_response, session_id):
    tickets = get_ticket_info(session_id, headers, cart_id)
    seats = []
    for ticket in tickets:
        seat = {
            'stand': ticket['tdc_section'],
            'row': ticket['tdc_seat_row'],
            'number': ticket['tdc_seat_number']
        }
        seats.append(seat)
    url = ipg_response.url
    return {'seats': seats, 'url': url}


def get_ticket_info(session_id, headers, cart_id):
    logged_response = get_logged(session_id, headers)
    sale_transaction_list = logged_response["sale_transactions"]
    tickets = []
    if len(sale_transaction_list) > 0:
        for sale_transaction in sale_transaction_list:
            if sale_transaction["id"] == cart_id:
                sale_transaction_customer_list = sale_transaction["sale_transaction_customers"]
                for sale_transaction_customer in sale_transaction_customer_list:
                    buyer_type_info_list = sale_transaction_customer["buyer_type_info"]
                    for buyer_type_info in buyer_type_info_list:
                        seats = buyer_type_info["seats"]
                        for seat in seats:
                            tickets.append(seat)
    return tickets