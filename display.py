import pygame
import requests
import multiprocessing

def load_orders():
    try:
        response = requests.get("http://localhost:8080/orders")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        return []

def display_food_orders(orders):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Food Orders")
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((235, 235, 235))
        y_offset = 20

        for order in orders:
            if any("food" in item["name"].lower() for item in order["items"]):
                text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
                screen.blit(text, (20, y_offset))
                y_offset += 40
                for item in order["items"]:
                    if "food" in item["name"].lower():
                        item_text = font.render(f"- {item['name']} x{item['quantity']}", True, (0, 0, 0))
                        screen.blit(item_text, (40, y_offset))
                        y_offset += 20

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def display_drink_orders(orders):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drink Orders")
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((235, 235, 235))
        y_offset = 20

        for order in orders:
            if any("drink" in item["name"].lower() for item in order["items"]):
                text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
                screen.blit(text, (20, y_offset))
                y_offset += 40
                for item in order["items"]:
                    if "drink" in item["name"].lower():
                        item_text = font.render(f"- {item['name']} x{item['quantity']}", True, (0, 0, 0))
                        screen.blit(item_text, (40, y_offset))
                        y_offset += 20

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def display_completed_orders(orders):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Completed Orders")
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((235, 235, 235))
        y_offset = 20

        for order in orders:
            if order["status"] == "complete":
                text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
                screen.blit(text, (20, y_offset))
                y_offset += 40
                for item in order["items"]:
                    item_text = font.render(f"- {item['name']} x{item['quantity']}", True, (0, 0, 0))
                    screen.blit(item_text, (40, y_offset))
                    y_offset += 20

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    orders = load_orders()
    if not orders:
        print("No orders to display.")
    else:
        food_process = multiprocessing.Process(target=display_food_orders, args=(orders,))
        drink_process = multiprocessing.Process(target=display_drink_orders, args=(orders,))
        completed_process = multiprocessing.Process(target=display_completed_orders, args=(orders,))

        food_process.start()
        drink_process.start()
        completed_process.start()

        food_process.join()
        drink_process.join()
        completed_process.join()
