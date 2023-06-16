package workflows

import (
	"go-worker/activities"
	"go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/workflow"
	"time"
)

func GoGreetingWorkflow(ctx workflow.Context, name string) (string, error) {
	ao := workflow.ActivityOptions{
		ScheduleToStartTimeout: 10 * time.Second,
		ScheduleToCloseTimeout: 15 * time.Second,
		RetryPolicy:            &temporal.RetryPolicy{MaximumAttempts: 2},
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	logger := workflow.GetLogger(ctx)
	logger.Info("GoGreetingWorkflow started", "name", name)

	var result string
	err := workflow.ExecuteActivity(ctx, activities.GoGreetingActivity, "Activity input").Get(ctx, &result)
	if err != nil {
		logger.Error("GoGreetingActivity failed.", "Error", err)
		return "", err
	}

	logger.Info("GoGreetingWorkflow completed.", "result", result)

	return result, nil
}
