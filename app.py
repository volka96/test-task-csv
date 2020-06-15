import sys
import csv
import datetime

try:
    file_path = sys.argv[1]
except IndexError:
    file_path = 'Orders.csv'


def get_products_data_from_csv(file_obj):
    reader = csv.DictReader(file_obj, delimiter=';')
    products_data = {}
    for line in reader:
        product_id = line["Product ID"]
        deal_data = {
            'order_date': line["Order Date"],
            'ship_date': line["Ship Date"],
            'sales': line["Sales"],
            'quantity': line["Quantity"],
            'profit': line["Profit"],
        }
        if product_id in products_data:
            products_data[product_id]['deals'].append(deal_data)

            products_data[product_id]['sales'] += float(deal_data['sales'].replace(',', '.'))
            products_data[product_id]['quantity'] += float(deal_data['quantity'].replace(',', '.'))
            products_data[product_id]['profit'] += float(deal_data['profit'].replace(',', '.'))

        else:
            products_data[product_id] = {'deals': [deal_data, ],
                                         'sales': float(deal_data['sales'].replace(',', '.')),
                                         'quantity': float(deal_data['quantity'].replace(',', '.')),
                                         'profit': float(deal_data['profit'].replace(',', '.'))}
    return products_data


def find_best_and_worth_product(products_data, field_name):
    best_product_id = None
    best_product_value = None

    worth_product_id = None
    worth_product_value = None

    for product_id in products_data:
        product_total_value = products_data[product_id][field_name]

        if not best_product_value or product_total_value > best_product_value:
            best_product_value = product_total_value
            best_product_id = product_id

        if not worth_product_value or product_total_value < worth_product_value:
            worth_product_value = product_total_value
            worth_product_id = product_id

    return best_product_id, worth_product_id


def find_average_delivery_time(products_data):
    total_delivery_days = 0
    n = 0
    for product_id in products_data:
        for deal in products_data[product_id]['deals']:
            date_oder_str = deal['order_date']
            if '/' in date_oder_str:
                date_oder_str = '{0}20{1}'.format(date_oder_str[:-2], date_oder_str[-2:])
                date_oder = datetime.datetime.strptime(date_oder_str, "%m/%d/%Y")
            else:
                date_oder = datetime.datetime.strptime(date_oder_str, "%d.%m.%Y")

            date_ship_str = deal['ship_date']
            if '/' in date_ship_str:
                date_ship_str = '{0}20{1}'.format(date_ship_str[:-2], date_ship_str[-2:])
                date_ship = datetime.datetime.strptime(date_ship_str, "%m/%d/%Y")
            else:
                date_ship = datetime.datetime.strptime(date_ship_str, "%d/%m/%Y")

            total_delivery_days += (date_ship - date_oder).days
            n += 1
    return total_delivery_days / n


def find_average_delivery_time_discrepancy(products_data, average_delivery_time):
    total_discrepancy_days = 0
    n = 0
    for product_id in products_data:
        for deal in products_data[product_id]['deals']:
            date_oder_str = deal['order_date']
            if '/' in date_oder_str:
                date_oder_str = '{0}20{1}'.format(date_oder_str[:-2], date_oder_str[-2:])
                date_oder = datetime.datetime.strptime(date_oder_str, "%m/%d/%Y")
            else:
                date_oder = datetime.datetime.strptime(date_oder_str, "%d.%m.%Y")

            date_ship_str = deal['ship_date']
            if '/' in date_ship_str:
                date_ship_str = '{0}20{1}'.format(date_ship_str[:-2], date_ship_str[-2:])
                date_ship = datetime.datetime.strptime(date_ship_str, "%m/%d/%Y")
            else:
                date_ship = datetime.datetime.strptime(date_ship_str, "%d/%m/%Y")

            total_discrepancy_days += abs(average_delivery_time - (date_ship - date_oder).days)
            n += 1
    return total_discrepancy_days / n


with open(file_path) as f_obj:
    products = get_products_data_from_csv(f_obj)

    print('Best and worth sales products: ', find_best_and_worth_product(products, 'sales'))
    print('Best and worth quantity products: ', find_best_and_worth_product(products, 'quantity'))
    print('Best and worth profit products: ', find_best_and_worth_product(products, 'profit'))

    average_delivery_time = find_average_delivery_time(products)
    print('Average delivery : ', average_delivery_time, ' day(s)')
    print('Average discrepancy : ', find_average_delivery_time_discrepancy(products, average_delivery_time), ' day(s)')

    with open("result.csv", "w") as f:
        f.write('Product ID;Sales;Quantity;Profit\n')
        for product_id in products:
            product_data = products[product_id]
            f.write('{0};{1};{2};{3}\n'.format(product_id,
                                               product_data['sales'],
                                               product_data['quantity'],
                                               product_data['profit']))
    f.close()



