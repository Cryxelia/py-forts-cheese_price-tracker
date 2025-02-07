from datetime import datetime

def ready_to_add():
    data = []  

    with open('text.txt', 'r', encoding="utf-8") as file: #utf-8 = to include characters like åäö
        for line in file:
            line = line.strip()

            name = None 
            #searches for the strimng and returns the possition of the first character
            name_start = line.find('a aria-label="') 
            if name_start != -1:
                #holds the length of the string so it points on the first character after the string
                name_start += len('a aria-label="')
                #looks for " after name start so it indiccates the end of the name
                name_end = line.find('"', name_start)
                #slicing to extract the portion between start and end
                name = line[name_start:name_end]

            price = None
            price_start = line.find('L7"><span>')
            if price_start != -1:
                price_start += len('L7"><span>')
                price_end = line.find('</span>', price_start)
                price = line[price_start:price_end]

            if name and price:
                fetched_date = datetime.now().strftime("%Y-%m-%d")
                cheese = {"name": name, "price": price, "date_added": fetched_date}
                data.append(cheese)
                
    return data

