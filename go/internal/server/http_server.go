package server

import (
	"encoding/json"
	"fmt"
	"net/http"
	"vtol-controller/internal/controller"
)

type HTTPServer struct {
	engine *controller.EmergencyEngine
	port   int
}

type SensorUpdateRequest struct {
	BatteryPercent float64 `json:"battery_percent"`
	DistanceToHome float64 `json:"distance_to_home"`
	WindSpeed      float64 `json:"wind_speed"`
}

type StatusResponse struct {
	Mode            string             `json:"mode"`
	ReturnTriggered bool               `json:"return_triggered"`
	Thresholds      map[string]float64 `json:"thresholds"`
}

func NewHTTPServer(engine *controller.EmergencyEngine, port int) *HTTPServer {
	return &HTTPServer{
		engine: engine,
		port:   port,
	}
}

func (s *HTTPServer) Start() error {
	http.HandleFunc("/api/v1/sensor/update", s.handleSensorUpdate)
	http.HandleFunc("/api/v1/status", s.handleGetStatus)
	http.HandleFunc("/api/v1/reset", s.handleReset)

	addr := fmt.Sprintf(":%d", s.port)
	fmt.Printf("[ INFO ] Controller listening on http://localhost%s\n", addr)
	fmt.Printf("   POST /api/v1/sensor/update - Send sensor data\n")
	fmt.Printf("   GET  /api/v1/status        - Get current status\n")
	fmt.Printf("   POST /api/v1/reset         - Reset controller\n")
	return http.ListenAndServe(addr, nil)
}

func (s *HTTPServer) handleSensorUpdate(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req SensorUpdateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	fmt.Printf("[ INFO ] Received sensor update: Battery=%.1f%%, Distance=%.2fkm, Wind=%.1fkm/h\n",
		req.BatteryPercent, req.DistanceToHome, req.WindSpeed)

	var mode controller.FlightMode

	// Update only the sensors that have meaningful values
	// (non-zero values indicate the sensor actually sent data)
	if req.BatteryPercent > 0 {
		mode = s.engine.UpdateBattery(req.BatteryPercent)
	}
	if req.DistanceToHome > 0 {
		mode = s.engine.UpdateDistance(req.DistanceToHome)
	}
	if req.WindSpeed > 0 {
		mode = s.engine.UpdateWind(req.WindSpeed)
	}

	status := s.engine.GetStatus()
	response := StatusResponse{
		Mode:            string(mode),
		ReturnTriggered: status["return_triggered"].(bool),
		Thresholds:      status["thresholds"].(map[string]float64),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func (s *HTTPServer) handleGetStatus(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	status := s.engine.GetStatus()

	response := StatusResponse{
		Mode:            status["mode"].(string),
		ReturnTriggered: status["return_triggered"].(bool),
		Thresholds:      status["thresholds"].(map[string]float64),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func (s *HTTPServer) handleReset(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	s.engine.Reset()

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{"status": "reset"})
}
