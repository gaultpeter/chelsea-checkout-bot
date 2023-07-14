import datetime
import json
import threading
import os

from login import get_logged
from seating import get_seating
from checkout_handler import sale_transaction_put, post_checkout


def start_checkout(session_id, event_id, headers, supporter_numbers, csrf, login_response):
    seating_response = get_seating(session_id, event_id, headers)
    threads = []
    for stand_id, stand_data in seating_response.items():
        if stand_data.get("prices").get("ADULT"):
            t = threading.Thread(target=checkout, args=(session_id, event_id, stand_id, supporter_numbers,
                                                        stand_data, headers, csrf, login_response))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()


def checkout(session_id, event_id, stand_id, supporter_numbers, stand_data, headers, csrf, login_response):
    print(f"Checking out tickets in: {stand_data['name']}")
    checkout_response = post_checkout(session_id, stand_id, event_id, supporter_numbers, stand_data, headers)
    if checkout_response.status_code == 201:
        cart_id = json.loads(checkout_response.text)['id']
        sale_transaction_put_response = sale_transaction_put(cart_id, session_id, csrf, login_response)
        if sale_transaction_put_response.status_code == 200:
            print("Successful checkout...")
            display_tickets(cart_id, headers, session_id)


def display_tickets(cart_id, headers, session_id):
    now = datetime.datetime.now()
    expiry_time = (now + datetime.timedelta(minutes=10)).strftime("%H:%M:%S")
    cart_url = f"https://chelseafc.3ddigitalvenue.com/buy-tickets/checkout;transaction={cart_id};flow=tickets"
    tickets = get_ticket_info(session_id, headers, cart_id)
    ticket_info = "\n".join([f"Stand: {ticket['tdc_section']} Row: {ticket['tdc_seat_row']} Seat number: "
                             f"{ticket['tdc_seat_number']}" for ticket in tickets])
    ticket_info += "\n" + "Expires: " + expiry_time
    ticket_info += "\n" + cart_url + "\n"
    with open("carts.txt", "a") as cart_file:
        cart_file.write(ticket_info)
        cart_file.write("\n")
    print(ticket_info)


def get_ticket_info(session_id, headers, cart_id):
    logged_response = json.loads(get_logged(session_id, headers).text)
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
