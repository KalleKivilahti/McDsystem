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