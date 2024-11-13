import requests

def load_orders():
    try:
        response = requests.get("http://localhost:8080/orders")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        return []
    
def confirm_item(order_id, item_index):
    """Send confirmation for a specific item in an order."""
    url = "http://localhost:8080/confirm_item"
    data = {"order_id": order_id, "item_index": item_index}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error confirming item in order {order_id}: {e}")
