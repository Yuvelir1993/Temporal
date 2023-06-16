package activities

import (
	"context"
	"go.temporal.io/sdk/activity"
)

func GreetingActivity(ctx context.Context, name string) (string, error) {
	logger := activity.GetLogger(ctx)
	logger.Info("GreetingActivity", "name", name)
	return "Hello " + name + "!", nil
}
