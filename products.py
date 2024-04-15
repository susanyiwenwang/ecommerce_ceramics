import json

# create list with dictionary of product names and image filepaths.
# save list as file in static directory
# create a function to add or delete from list.

product_list = []


def add_product(name, img_fp):
    new_product = {"name": name, "img": img_fp}
    # product_list.append(new_product)
    try:
        with open("static/products.json", "r") as data_file:
            data = json.load(data_file)
            print(data)
            data.update(new_product)
            print(data)
        with open("static/products.json", "w") as data_file:
            json.dump(new_product, data_file, indent=4)
    except json.decoder.JSONDecodeError:
        with open("static/products.json", "w") as data_file:
            json.dump(new_product, data_file, indent=4)


add_product("Turqouise Plate", "turkis_plate.jpg")


