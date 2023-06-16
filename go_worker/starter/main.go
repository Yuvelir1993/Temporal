package main

import (
	"context"
	"github.com/google/uuid"
	"go-worker/commons"
	"go-worker/workflows"
	"log"

	"go.temporal.io/sdk/client"
)

func main() {
	// The client is a heavyweight object that should be created once per process.
	c, err := client.Dial(client.Options{})
	if err != nil {
		log.Fatalln("Unable to create client", err)
	}
	defer c.Close()

	uuid4, nil := uuid.NewUUID()

	workflowOptions := client.StartWorkflowOptions{
		ID:        "go-" + uuid4.String(),
		TaskQueue: commons.TaskQueuePolyglot,
	}

	we, err := c.ExecuteWorkflow(context.Background(), workflowOptions, workflows.GoGreetingWorkflow, "Temporal")
	if err != nil {
		log.Fatalln("Unable to execute workflow", err)
	}

	log.Println("Started workflow", "WorkflowID", we.GetID(), "RunID", we.GetRunID())

	// Synchronously wait for the workflow completion.
	var result string
	err = we.Get(context.Background(), &result)
	if err != nil {
		log.Fatalln("Unable get workflow result", err)
	}
	log.Println("GoGreetingWorkflow result:", result)
}
