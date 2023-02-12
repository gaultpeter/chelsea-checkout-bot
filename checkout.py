import json
import threading

from login import get_logged
from seating import get_seating
from checkout_handler import sale_transaction_put, post_checkout
from ipg_online_payment import ipg_online_payment_processing


def start_checkout(session_id, event_id, headers, customer_ids, csrf, login_response):
    seating_response = get_seating(session_id, event_id, headers)
    threads = []
    for stand_id, stand_data in seating_response.items():
        if stand_data.get("prices").get("ADULT"):
            t = threading.Thread(target=checkout, args=(session_id, event_id, stand_id, customer_ids,
                                                        stand_data, headers, csrf, login_response))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()


def checkout(session_id, event_id, stand_id, customer_ids, stand_data, headers, csrf, login_response):
    print(f"Checking out tickets in: {stand_data['name']}")
    checkout_response = post_checkout(session_id, stand_id, event_id, customer_ids, stand_data, headers)
    if checkout_response.status_code==201:
        cart_id = json.loads(checkout_response.text)['id']
        sale_transaction_put_response = sale_transaction_put(cart_id, session_id, csrf, login_response)
        if sale_transaction_put_response.status_code==200:
            sale_transaction_response = json.loads(sale_transaction_put_response.text)
            ipg_online_payment_processing_response = ipg_online_payment_processing(sale_transaction_response)
            display_tickets(cart_id, headers, ipg_online_payment_processing_response, session_id)


def display_tickets(cart_id, headers, ipg_response, session_id):
    tickets = get_ticket_info(session_id, headers, cart_id)
    ticket_info = "\n".join([f"Stand: {ticket['tdc_section']} Row: {ticket['tdc_seat_row']} Seat number: "
                             f"{ticket['tdc_seat_number']}" for ticket in tickets])
    ticket_info += "\n" + ipg_response.url + "\n"
    print(ticket_info)


def get_ticket_info(session_id, headers, cart_id):
    logged_response = json.loads(get_logged(session_id, headers).text)
    sale_transaction_list = logged_response["sale_transactions"]
    tickets = []
    if len(sale_transaction_list)>0:
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


