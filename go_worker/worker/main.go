package main

import (
	"go-worker/activities"
	"go-worker/workflows"
	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"log"
)

func main() {
	// The client and worker are heavyweight objects that should be created once per process.
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

	w := worker.New(c, "go-worker-task-queue", worker.Options{})

	w.RegisterWorkflow(workflows.Workflow)
	w.RegisterActivity(activities.GreetingActivity)

	err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start worker", err)
	}
}
