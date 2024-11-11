import pygame
import requests
import json

def load_orders():
    try:
        response = requests.get("http://localhost:8080/orders")
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        return []

def complete_order(order_id):
    url = "http://localhost:8080/complete_order"
    data = {"order_id": order_id}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error completing order {order_id}: {e}")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Order Processing System")

font = pygame.font.Font(None, 36)

def display_orders(orders):
    screen.fill((235, 235, 235))

    y_offset = 20

    for i, order in enumerate(orders):
        text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
        screen.blit(text, (20, y_offset))
        y_offset += 40
        for item in order['items']:
            item_text = font.render(f"- {item['name']} x{item['quantity']}", True, (0, 0, 0))
            screen.blit(item_text, (40, y_offset))
            y_offset += 20

            customizations = item.get('customizations', [])
            if customizations:
                for customization in customizations:
                    customization_text = font.render(f"  * {customization}", True, (0, 0, 0))
                    screen.blit(customization_text, (60, y_offset))
                    y_offset += 20

    pygame.display.flip()

running = True
orders = load_orders()

if not orders:
    print("No orders to display.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for order in orders:
                    if order["status"] == "processing":
                        complete_order(order["order_id"])
                        order["status"] = "complete" 

    if orders:
        display_orders(orders)

pygame.quit()
