package helpers

type Item struct {
	Name           string   `json:"name"`
	Quantity       int      `json:"quantity"`
	Customizations []string `json:"customizations,omitempty"`
	Category       string   `json:"category"`
	Confirmed      bool     `json:"confirmed"`
}

type Order struct {
	OrderID string `json:"order_id"`
	Status  string `json:"status"`
	Items   []Item `json:"items"`
}
