package workflows

import (
	"go-worker/activities"
	"go-worker/commons"
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

	pao := workflow.ActivityOptions{
		ScheduleToStartTimeout: 10 * time.Second,
		ScheduleToCloseTimeout: 15 * time.Second,
		RetryPolicy:            &temporal.RetryPolicy{MaximumAttempts: 2},
		TaskQueue:              commons.TaskQueuePython,
	}
	ctx = workflow.WithActivityOptions(ctx, pao)

	var pythonActivityResult string
	perr := workflow.ExecuteActivity(ctx, commons.PythonGreetingActivity, "Hello from Go to the "+commons.PythonGreetingActivity+"!").Get(ctx, &pythonActivityResult)
	if perr != nil {
		logger.Error("PythonGreetingActivity failed.", "Error", err)
		return "", perr
	}

	logger.Info("GoGreetingWorkflow completed.", "result", result)
	logger.Info("PythonGreetingActivity completed.", "pythonActivityResult", pythonActivityResult)

	return result, nil
}
