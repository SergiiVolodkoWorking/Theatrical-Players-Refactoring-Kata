import math


def format_as_dollars(amount):
    return f"${amount:0,.2f}"

def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0

    result = f'Statement for {invoice["customer"]}\n'

    for performance in invoice['performances']:
        if not performance['playID'] in plays:
            continue
        play = plays[performance['playID']]

        tragedy_minimum_amount = 400
        tragedy_additional_seat_price = 10
        tragedy_seats_limit = 30

        comedy_minimum_amount = 300
        comedy_additional_seat_price = 5
        comedy_extra_seats_one_time_fee = 100
        comedy_seats_limit = 20
        comedy_regular_seat_price = 3
        performance_total = 0

        if play['type'] == "tragedy":
            performance_total = tragedy_minimum_amount
            if performance['audience'] > tragedy_seats_limit:
                additional_seats = performance['audience'] - tragedy_seats_limit
                performance_total += tragedy_additional_seat_price * additional_seats
        elif play['type'] == "comedy":
            performance_total = comedy_minimum_amount
            if performance['audience'] > comedy_seats_limit:
                performance_total += comedy_extra_seats_one_time_fee
                additional_seats = performance['audience'] - comedy_seats_limit
                performance_total += comedy_additional_seat_price * additional_seats

            performance_total += comedy_regular_seat_price * performance['audience']

        else:
            raise ValueError(f'unknown type: {play["type"]}')

        # add volume credits
        volume_credits += max(performance['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += math.floor(performance['audience'] / 5)
        # print line for this order
        result += f' {play["name"]}: {format_as_dollars(performance_total)} ({performance["audience"]} seats)\n'
        total_amount += performance_total

    result += f'Amount owed is {format_as_dollars(total_amount)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result


