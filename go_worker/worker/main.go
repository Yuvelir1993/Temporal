package main

import (
	"go-worker/activities"
	"go-worker/commons"
	"go-worker/workflows"
	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"go.temporal.io/sdk/workflow"
	"log"
)

func main() {
	// The client and worker are heavyweight objects that should be created once per process.
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

	w := worker.New(c, commons.TaskQueuePolyglot, worker.Options{})

	w.RegisterWorkflowWithOptions(workflows.GoGreetingWorkflow, workflow.RegisterOptions{Name: commons.GoGreetingWorkflow})
	w.RegisterActivityWithOptions(activities.GoGreetingActivity, activity.RegisterOptions{Name: commons.GoGreetingActivity})

	err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start worker", err)
	}
}
