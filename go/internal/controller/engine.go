package controller

import (
	"log"
	"sync"
)

// FlightMode represents the current state
type FlightMode string

const (
	ModeNormal          FlightMode = "NORMAL"
	ModeEmergencyReturn FlightMode = "EMERGENCY_RETURN"
)

// SensorData represents data from all sensors
type SensorData struct {
	BatteryPercent float64
	DistanceToHome float64 // km
	WindSpeed      float64 // km/h
}

// EmergencyEngine contains the business logic
type EmergencyEngine struct {
	mu              sync.RWMutex
	currentMode     FlightMode
	returnTriggered bool

	// Thresholds
	criticalBattery float64
	maxDistance     float64
	maxWind         float64

	// Store latest values from each sensor
	lastBattery  float64
	lastDistance float64
	lastWind     float64
}

// NewEmergencyEngine creates a new engine
func NewEmergencyEngine() *EmergencyEngine {
	return &EmergencyEngine{
		currentMode:     ModeNormal,
		returnTriggered: false,
		criticalBattery: 20.0,
		maxDistance:     2.0,
		maxWind:         35.0,
		lastBattery:     100.0,
		lastDistance:    0.0,
		lastWind:        0.0,
	}
}

// UpdateBattery processes battery sensor data
func (e *EmergencyEngine) UpdateBattery(percent float64) FlightMode {
	e.mu.Lock()
	defer e.mu.Unlock()

	log.Printf("[ INFO ] Battery update: %.1f%%", percent)
	e.lastBattery = percent
	return e.evaluateConditions()
}

// UpdateDistance processes GPS sensor data
func (e *EmergencyEngine) UpdateDistance(distance float64) FlightMode {
	e.mu.Lock()
	defer e.mu.Unlock()

	log.Printf("[ INFO ] GPS update: %.2fkm", distance)
	e.lastDistance = distance
	return e.evaluateConditions()
}

// UpdateWind processes wind sensor data
func (e *EmergencyEngine) UpdateWind(wind float64) FlightMode {
	e.mu.Lock()
	defer e.mu.Unlock()

	log.Printf("[ INFO ] Wind update: %.1fkm/h", wind)
	e.lastWind = wind
	return e.evaluateConditions()
}

// evaluateConditions checks if emergency return should be triggered
// Returns current mode after evaluation
func (e *EmergencyEngine) evaluateConditions() FlightMode {
	// If already in emergency, stay there
	if e.currentMode == ModeEmergencyReturn {
		log.Printf("[ INFO ] Already in emergency mode, staying")
		return e.currentMode
	}

	// Check emergency conditions
	isBatteryCritical := e.lastBattery < e.criticalBattery
	log.Printf("[ INFO ] Battery critical? %v (%.1f < %.1f)",
		isBatteryCritical, e.lastBattery, e.criticalBattery)

	if isBatteryCritical {
		isDistanceExceeded := e.lastDistance > e.maxDistance
		isWindExceeded := e.lastWind > e.maxWind

		log.Printf("[ INFO ] Distance exceeded? %v (%.2f > %.1f)",
			isDistanceExceeded, e.lastDistance, e.maxDistance)
		log.Printf("[ INFO ] Wind exceeded? %v (%.1f > %.1f)",
			isWindExceeded, e.lastWind, e.maxWind)

		if isDistanceExceeded || isWindExceeded {
			log.Printf("[ INFO ] EMERGENCY RETURN TRIGGERED!")
			e.currentMode = ModeEmergencyReturn
			e.returnTriggered = true
		} else {
			log.Printf("[ INFO ] Secondary conditions not met, staying in normal mode")
		}
	} else {
		log.Printf("[ INFO ] Battery not critical, staying in normal mode")
	}

	log.Printf("[ INFO ] Final mode: %s", e.currentMode)
	return e.currentMode
}

// GetStatus returns current status
func (e *EmergencyEngine) GetStatus() map[string]interface{} {
	e.mu.RLock()
	defer e.mu.RUnlock()

	return map[string]interface{}{
		"mode":             string(e.currentMode),
		"return_triggered": e.returnTriggered,
		"thresholds": map[string]float64{
			"critical_battery": e.criticalBattery,
			"max_distance":     e.maxDistance,
			"max_wind":         e.maxWind,
		},
		"last_values": map[string]float64{
			"battery":  e.lastBattery,
			"distance": e.lastDistance,
			"wind":     e.lastWind,
		},
	}
}

// Reset resets the engine state
func (e *EmergencyEngine) Reset() {
	e.mu.Lock()
	defer e.mu.Unlock()

	log.Println("[ INFO ] Resetting controller")
	e.currentMode = ModeNormal
	e.returnTriggered = false
	e.lastBattery = 100.0
	e.lastDistance = 0.0
	e.lastWind = 0.0
}
