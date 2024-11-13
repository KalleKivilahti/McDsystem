package helpers

import (
	"sync"
	"time"
)

func Workers(id int, orders <-chan *Order, wg *sync.WaitGroup) {
	defer wg.Done()
	if id != 0 {
		for order := range orders {
			Mu.Lock()
			order.Status = "pending"
			Mu.Unlock()
			time.Sleep(1 * time.Second)
		}
	}
}
