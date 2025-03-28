from datetime import datetime, timedelta

def parse_line(line):
    parts = line.strip().split(',')
    if len(parts) != 3:
        return None
    product = parts[0].strip()
    date_str = parts[1].strip()
    price_str = parts[2].strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        price = float(price_str)
    except (ValueError, TypeError):
        return None
    return (product, date, price)

def read_data(filename):
    data = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    data.append(parsed)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []
    return data

def filter_last_month(data, product_name, today):
    start_date = today - timedelta(days=30)
    filtered = []
    for entry in data:
        product, date, price = entry
        if product == product_name and date >= start_date:
            filtered.append((date, price))
    filtered.sort(key=lambda x: x[0])
    return filtered

def get_price_change(filename, product_name, today=None):
    if today is None:
        today = datetime.now().date()
    data = read_data(filename)
    filtered = filter_last_month(data, product_name, today)
    if len(filtered) < 1:
        return None
    earliest_price = filtered[0][1]
    latest_price = filtered[-1][1]
    return latest_price - earliest_price

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Calculate price change for a product over the last month.')
    parser.add_argument('filename', type=str, help='Path to the input .txt file')
    parser.add_argument('product', type=str, help='Product name to analyze')
    args = parser.parse_args()
    change = get_price_change(args.filename, args.product)
    if change is not None:
        print(f"The price change for '{args.product}' over the last month is: {change:.2f}")
    else:
        print(f"No data available for '{args.product}' in the last month.")