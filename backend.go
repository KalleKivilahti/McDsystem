package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type Order struct {
	OrderID string `json:"order_id"`
	Status  string `json:"status"`
	Items   []struct {
		Name           string   `json:"name"`
		Quantity       int      `json:"quantity"`
		Customizations []string `json:"customizations,omitempty"`
	} `json:"items"`
}

var orders []Order
var mu sync.Mutex

func worker(id int, orders <-chan *Order, wg *sync.WaitGroup) {
	defer wg.Done()
	for order := range orders {
		mu.Lock()
		order.Status = "processing"
		mu.Unlock()

		time.Sleep(2 * time.Second)
	}
}

func ServeOrders(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(orders)
}

func CompleteOrder(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	var orderData Order
	err := json.NewDecoder(r.Body).Decode(&orderData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	for i := range orders {
		if orders[i].OrderID == orderData.OrderID {
			orders[i].Status = "complete"
			break
		}
	}

	w.WriteHeader(http.StatusOK)
}

// data to Order struct
func LoadOrders(filename string) ([]Order, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var orders []Order
	err = json.Unmarshal(data, &orders)
	return orders, err
}

func main() {
	var err error
	orders, err = LoadOrders("orders.json")
	if err != nil {
		panic(err)
	}

	numWorkers := 5
	orderChannel := make(chan *Order)
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker(i, orderChannel, &wg)
	}

	// workers
	go func() {
		for i := range orders {
			orderChannel <- &orders[i]
		}
		close(orderChannel)
	}()

	// API
	http.HandleFunc("/orders", ServeOrders)
	http.HandleFunc("/complete_order", CompleteOrder)
	fmt.Println("Server is running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)

	wg.Wait()
}
