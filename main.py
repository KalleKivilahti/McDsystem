import loadconfirmorders as load
import display as dsp
import multiprocessing


def main(): 
    orders = load.load_orders()
    if not orders:
        print("No orders to display.")
    else:
        food_process = multiprocessing.Process(target=dsp.display_food_orders, args=(orders,))
        drink_process = multiprocessing.Process(target=dsp.display_drink_orders, args=(orders,))
        completed_process = multiprocessing.Process(target=dsp.display_completed_orders, args=(orders,))

        food_process.start()
        drink_process.start()
        completed_process.start()

        food_process.join()
        drink_process.join()
        completed_process.join()

if __name__ == "__main__":
    main()