package main

import (
	"fmt"
	"log"
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
	orderChannel := make(chan *helpers.Order) // channel of pointers to Order struct
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go helpers.Workers(i, orderChannel, &wg)
	}

	// workers iterate over Orders and sends each order to orderchannel
	go func() {
		for i := range helpers.Orders {
			orderChannel <- &helpers.Orders[i]
		}
		close(orderChannel)
	}() // () <- calls the function func immediately otherwise it would be only defined

	// API
	http.HandleFunc("/orders", helpers.ServeOrders)
	http.HandleFunc("/confirm_item", helpers.ConfirmItem)
	http.HandleFunc("/complete_order", helpers.CompleteOrder)
	fmt.Println("Server is running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err) // log any errors starting the server
	}

	wg.Wait()
}
