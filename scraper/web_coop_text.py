from datetime import datetime

def get_name(line):
    #searches for the string and returns the possition of the first character
    name_start = line.find('a aria-label="')
    if name_start != -1:
        #holds the length of the string so it points on the first character after the string
        name_start += len('a aria-label="')
        #looks for " after name start so it indicates the end of the name
        name_end = line.find('"', name_start)
        #slicing to extract the portion between start and end
        return line[name_start:name_end]


def get_price(line):
    price_start = line.find('L7"><span>')
    if price_start != -1:
        price_start += len('L7"><span>')
        price_end = line.find('</span>', price_start)
        return line[price_start:price_end]

def finished_product(line):
    name = get_name(line)
    price = get_price(line)
    if name and price:
        return {
            "name": name,
            "price": price,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }

def read_file(filename):
    data = []
    with open(filename, 'r', encoding="utf-8") as file:
        for line in file:
            cheese = finished_product(line.strip())
            if cheese:
                data.append(cheese)
    return data
