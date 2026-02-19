package main

import (
	"flag"
	"fmt"
	"log"
	"vtol-controller/internal/controller"
	"vtol-controller/internal/server"
)

func main() {
	port := flag.Int("port", 8080, "HTTP server port")
	flag.Parse()

	log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds)

	fmt.Println("[ INFO ] VTOL Emergency Controller Starting...")
	fmt.Printf("[ INFO ] Listening on port %d\n", *port)
	fmt.Println("[ INFO ] Waiting for sensor data...")

	engine := controller.NewEmergencyEngine()
	srv := server.NewHTTPServer(engine, *port)

	if err := srv.Start(); err != nil {
		log.Fatal("[ ERROR ] Server failed:", err)
	}
}
