from storage import select_js

def select():
    list_js = select_js()
    for products in list_js:
        for keys , values in products.items():
            print(f"{keys} : {values}")
