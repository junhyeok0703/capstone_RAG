import json

# Read the provided JSON file
file_path = '가격데이터넣은sample.json'
with open(file_path, 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Function to calculate and update total prices in the dataset
def update_total_prices(quotes):
    for quote in quotes:
        total_price = 0
        for part in quote['parts_price'].values():
            price = int(part['가격'].replace('원', '').replace(',', ''))
            quantity = int(part['수량'])
            total_price += price * quantity
        quote['total_price'] = f"{total_price}원"

    return quotes

# Update the quotes with new total prices
updated_quotes = update_total_prices(quotes_data)

# Write the updated data back to a new JSON file
output_file_path = '총가격데이터sample.json'
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(updated_quotes, file, indent=4, ensure_ascii=False)

output_file_path  # Output the path to the updated file
