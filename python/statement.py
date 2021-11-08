import math


PLAY_TYPE_COMEDY = "comedy"
PLAY_TYPE_TRAGEDY = "tragedy"


def format_as_dollars(amount):
    return f"${amount:0,.2f}"


def calculate_performance_total_amount(play_type: str, occupied_seats_count: int):
    tragedy_minimum_amount = 400
    tragedy_additional_seat_price = 10
    tragedy_seats_limit = 30

    comedy_minimum_amount = 300
    comedy_additional_seat_price = 5
    comedy_extra_seats_one_time_fee = 100
    comedy_seats_limit = 20
    comedy_regular_seat_price = 3

    performance_total = 0

    if play_type == PLAY_TYPE_TRAGEDY:
        performance_total = tragedy_minimum_amount
        if occupied_seats_count > tragedy_seats_limit:
            additional_seats_count = occupied_seats_count - tragedy_seats_limit
            performance_total += tragedy_additional_seat_price * additional_seats_count
    elif play_type == PLAY_TYPE_COMEDY:
        performance_total = comedy_minimum_amount
        if occupied_seats_count > comedy_seats_limit:
            performance_total += comedy_extra_seats_one_time_fee
            additional_seats_count = occupied_seats_count - comedy_seats_limit
            performance_total += comedy_additional_seat_price * additional_seats_count

        performance_total += comedy_regular_seat_price * occupied_seats_count
    else:
        raise ValueError(f'unknown type: {play_type}')
    return performance_total


def calculate_volume_credits(play_type: str, occupied_seats_count: int):
    volume_credits = 0

    regular_seats_capacity = 30
    additional_seats = occupied_seats_count - regular_seats_capacity
    if additional_seats > 0:
        volume_credits += additional_seats

    if play_type == PLAY_TYPE_COMEDY:
        seats_group_size = 5
        volume_credits += math.floor(occupied_seats_count / seats_group_size)
    return volume_credits


def statement(invoice, plays):
    total_amount = 0
    total_volume_credits = 0

    performances_for_report = []
    for performance in invoice['performances']:
        if not performance['playID'] in plays:
            continue
        play = plays[performance['playID']]
        play_name = play['name']
        play_type = play['type']
        occupied_seats_count = performance['audience']

        amount = calculate_performance_total_amount(play_type, occupied_seats_count)
        total_amount += amount
        total_volume_credits += calculate_volume_credits(play_type, occupied_seats_count)

        performances_for_report.append({
            "play_name": play_name,
            "play_type": play_type,
            "occupied_seats_count": occupied_seats_count,
            "amount": amount,
        })


    customer_name = invoice["customer"]
    result = f'Statement for {customer_name}\n'

    for p in performances_for_report:
        result += f' {p["play_name"]}: {format_as_dollars(p["amount"])} ({p["occupied_seats_count"]} seats)\n'

    result += f'Amount owed is {format_as_dollars(total_amount)}\n'
    result += f'You earned {total_volume_credits} credits\n'
    return result
