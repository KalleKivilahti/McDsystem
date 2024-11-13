import pygame
import loadconfirmorders as load

clock = pygame.time.Clock()

def display_food_orders(orders):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Food Orders")
    font = pygame.font.Font(None, 36)
    running = True
    selected_order = 0  # Track which order is currently selected

    while running:
        screen.fill((235, 235, 235))
        y_offset = 20

        for order_index, order in enumerate(orders):
            if any(item["category"].lower() == "food" for item in order["items"]):
                text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
                screen.blit(text, (20, y_offset))
                y_offset += 40

                for item_index, item in enumerate(order["items"]):
                    if item["category"].lower() == "food":
                        color = (0, 255, 0) if item["confirmed"] else (255, 0, 0)  # Green if confirmed, red if not
                        item_text = font.render(f"- {item['name']} x{item['quantity']}", True, color)
                        screen.blit(item_text, (40, y_offset))
                        y_offset += 20

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to confirm the selected item
                    order = orders[selected_order]
                    for item_index, item in enumerate(order["items"]):
                        if item["category"].lower() == "food" and not item["confirmed"]:
                            load.confirm_item(order, item_index)  # Confirm the item
                            break  # Only confirm one item per Enter press
                elif event.key == pygame.K_DOWN:  # Move to next order
                    selected_order = (selected_order + 1) % len(orders)
                elif event.key == pygame.K_UP:  # Move to previous order
                    selected_order = (selected_order - 1) % len(orders)

        clock.tick(60)

    pygame.quit()

def display_drink_orders(orders):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drink Orders")
    font = pygame.font.Font(None, 36)
    running = True
    selected_order = 0  # Track which order is currently selected

    while running:
        screen.fill((235, 235, 235))
        y_offset = 20

        for order_index, order in enumerate(orders):
            if any(item["category"].lower() == "drink" for item in order["items"]):
                text = font.render(f"Order {order['order_id']}: {order['status']}", True, (0, 0, 0))
                screen.blit(text, (20, y_offset))
                y_offset += 40

                for item_index, item in enumerate(order["items"]):
                    if item["category"].lower() == "drink":
                        color = (0, 255, 0) if item["confirmed"] else (255, 0, 0)  # Green if confirmed, red if not
                        item_text = font.render(f"- {item['name']} x{item['quantity']}", True, color)
                        screen.blit(item_text, (40, y_offset))
                        y_offset += 20

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to confirm the selected item
                    order = orders[selected_order]
                    for item_index, item in enumerate(order["items"]):
                        if item["category"].lower() == "drink" and not item["confirmed"]:
                            load.confirm_item(order, item_index)  # Confirm the item
                            break  # Only confirm one item per Enter press
                elif event.key == pygame.K_DOWN:  # Move to next order
                    selected_order = (selected_order + 1) % len(orders)
                elif event.key == pygame.K_UP:  # Move to previous order
                    selected_order = (selected_order - 1) % len(orders)

        clock.tick(60)

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

        clock.tick(60)

    pygame.quit()