package main

import (
	"fmt"
	"mcdsystem/helpers"
	"net/http"
	"sync"
)

func main() {
	var err error
	helpers.Orders, err = helpers.LoadOrders("orders.json")
	if err != nil {
		panic(err)
	}

	numWorkers := 5
	orderChannel := make(chan *helpers.Order)
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go helpers.Workers(i, orderChannel, &wg)
	}

	// workers
	go func() {
		for i := range helpers.Orders {
			orderChannel <- &helpers.Orders[i]
		}
		close(orderChannel)
	}()

	// API
	http.HandleFunc("/orders", helpers.ServeOrders)
	http.HandleFunc("/complete_order", helpers.CompleteOrder)
	fmt.Println("Server is running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)

	wg.Wait()
}
