import concurrent.futures

from backend.checkout_handler import start_checkout


def start_script(session_id, event_id, headers, supporter_numbers, csrf, login_response, num_of_attempts):
    checkout_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(start_checkout, session_id, event_id, headers, supporter_numbers,
                                   csrf, login_response)
                   for _ in range(num_of_attempts)]
        for future in concurrent.futures.as_completed(futures):
            checkout_result = future.result()
            checkout_results.append(checkout_result)  # append the checkout result to the list
    return checkout_results


