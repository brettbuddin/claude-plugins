# Receiver Component

Import: `go.opentelemetry.io/collector/receiver`

Receivers collect telemetry data and push it to a consumer (the next component in the pipeline).
They receive a `consumer.Traces/Metrics/Logs` in the create function and push data to it.
They do NOT embed the consumer interface.

## Factory

```go
package myreceiver

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/consumer"
    "go.opentelemetry.io/collector/receiver"

    "github.com/org/repo/receiver/myreceiver/internal/metadata"
)

func NewFactory() receiver.Factory {
    return receiver.NewFactory(
        metadata.Type,
        createDefaultConfig,
        receiver.WithMetrics(createMetricsReceiver, metadata.MetricsStability),
        // receiver.WithTraces(createTracesReceiver, metadata.TracesStability),
        // receiver.WithLogs(createLogsReceiver, metadata.LogsStability),
    )
}

func createDefaultConfig() component.Config {
    return &Config{
        Endpoint: "localhost:4317",
    }
}

func createMetricsReceiver(
    _ context.Context,
    params receiver.Settings,
    cfg component.Config,
    consumer consumer.Metrics,
) (receiver.Metrics, error) {
    return newMetricsReceiver(params, cfg.(*Config), consumer)
}
```

## Create Function Signatures

```go
type CreateTracesFunc  func(context.Context, Settings, component.Config, consumer.Traces) (Traces, error)
type CreateMetricsFunc func(context.Context, Settings, component.Config, consumer.Metrics) (Metrics, error)
type CreateLogsFunc    func(context.Context, Settings, component.Config, consumer.Logs) (Logs, error)
```

## Receiver Interfaces

```go
type Traces  interface { component.Component }
type Metrics interface { component.Component }
type Logs    interface { component.Component }
```

A receiver just needs `Start(ctx, host) error` and `Shutdown(ctx) error`. It pushes data by
calling `consumer.ConsumeTraces/ConsumeMetrics/ConsumeLogs` on the consumer it received.

## Implementation Pattern

```go
package myreceiver

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/consumer"
    "go.opentelemetry.io/collector/receiver"
    "go.uber.org/zap"
)

type metricsReceiver struct {
    cfg      *Config
    logger   *zap.Logger
    consumer consumer.Metrics
    cancel   context.CancelFunc
}

func newMetricsReceiver(params receiver.Settings, cfg *Config, consumer consumer.Metrics) (*metricsReceiver, error) {
    return &metricsReceiver{
        cfg:      cfg,
        logger:   params.Logger,
        consumer: consumer,
    }, nil
}

func (r *metricsReceiver) Start(ctx context.Context, _ component.Host) error {
    ctx, r.cancel = context.WithCancel(ctx)
    // Start goroutines to collect data and call r.consumer.ConsumeMetrics(ctx, md)
    return nil
}

func (r *metricsReceiver) Shutdown(_ context.Context) error {
    if r.cancel != nil {
        r.cancel()
    }
    return nil
}
```

## metadata.yaml

```yaml
type: myreceiver
status:
  class: receiver
  stability:
    beta: [metrics]
    alpha: [traces, logs]
  distributions: [contrib]
  codeowners:
    active: [githubuser]
tests:
  config:
    endpoint: localhost:0
```
