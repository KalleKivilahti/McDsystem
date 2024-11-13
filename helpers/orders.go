package helpers

import (
	"encoding/json"
	"net/http"
	"os"
	"sync"
)

var Orders []Order
var Mu sync.Mutex // mutex lock prevents goroutines accessing same data same time

func CompleteOrder(w http.ResponseWriter, r *http.Request) {
	Mu.Lock()
	defer Mu.Unlock()

	var orderData Order
	err := json.NewDecoder(r.Body).Decode(&orderData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	for i := range Orders {
		if Orders[i].OrderID == orderData.OrderID {
			Orders[i].Status = "complete"
			break
		}
	}

	w.WriteHeader(http.StatusOK)
}

// format data to Order struct
func LoadOrders(filename string) ([]Order, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var Orders []Order
	err = json.Unmarshal(data, &Orders)
	return Orders, err
}

func ServeOrders(w http.ResponseWriter, r *http.Request) {
	Mu.Lock()
	defer Mu.Unlock()

	// states to HTTP response header the format is JSON
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(Orders)
}
