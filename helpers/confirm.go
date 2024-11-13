package helpers

import (
	"encoding/json"
	"net/http"
)

func ConfirmItem(w http.ResponseWriter, r *http.Request) {
	var req struct {
		OrderID   string `json:"order_id"`
		ItemIndex int    `json:"item_index"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	Mu.Lock()
	defer Mu.Unlock()

	var order *Order
	for i := range Orders {
		if Orders[i].OrderID == req.OrderID {
			order = &Orders[i]
			break
		}
	}

	if order == nil {
		http.Error(w, "Order not found", http.StatusNotFound)
		return
	}

	if req.ItemIndex < 0 || req.ItemIndex >= len(order.Items) {
		http.Error(w, "Invalid item index", http.StatusBadRequest)
		return
	}

	order.Items[req.ItemIndex].Confirmed = true

	allConfirmed := true
	for _, item := range order.Items {
		if !item.Confirmed {
			allConfirmed = false
			break
		}
	}

	if allConfirmed {
		order.Status = "complete"
	}

	response := struct {
		OrderID   string `json:"order_id"`
		ItemIndex int    `json:"item_index"`
		Confirmed bool   `json:"confirmed"`
		Status    string `json:"status"`
	}{
		OrderID:   req.OrderID,
		ItemIndex: req.ItemIndex,
		Confirmed: true,
		Status:    order.Status,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Error encoding response", http.StatusInternalServerError)
	}
}
