package activities

import (
	"context"
	"go.temporal.io/sdk/activity"
)

func GoGreetingActivity(ctx context.Context, input string) (string, error) {
	logger := activity.GetLogger(ctx)
	logger.Info("GoGreetingActivity", "name", input)
	return "Hello !!!!!! " + input, nil
}
