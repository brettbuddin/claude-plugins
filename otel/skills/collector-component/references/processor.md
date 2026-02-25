# Processor Component

Import: `go.opentelemetry.io/collector/processor`

Processors transform telemetry data. They embed the consumer interface (they ARE consumers)
and receive a "next consumer" to forward data to after processing.

## Factory

Use `processorhelper` for the standard pattern. It wraps your processing function and handles
observability, start/shutdown, and forwarding to the next consumer.

```go
package myprocessor

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/consumer"
    "go.opentelemetry.io/collector/processor"
    "go.opentelemetry.io/collector/processor/processorhelper"

    "github.com/org/repo/processor/myprocessor/internal/metadata"
)

var processorCapabilities = consumer.Capabilities{MutatesData: true}

func NewFactory() processor.Factory {
    return processor.NewFactory(
        metadata.Type,
        createDefaultConfig,
        processor.WithLogs(createLogsProcessor, metadata.LogsStability),
        processor.WithTraces(createTracesProcessor, metadata.TracesStability),
        processor.WithMetrics(createMetricsProcessor, metadata.MetricsStability),
    )
}

func createDefaultConfig() component.Config {
    return &Config{}
}

func createLogsProcessor(
    ctx context.Context,
    set processor.Settings,
    cfg component.Config,
    nextConsumer consumer.Logs,
) (processor.Logs, error) {
    p, err := newProcessor(cfg.(*Config), set.Logger)
    if err != nil {
        return nil, err
    }
    return processorhelper.NewLogs(
        ctx, set, cfg, nextConsumer,
        p.processLogs,
        processorhelper.WithCapabilities(processorCapabilities),
        processorhelper.WithStart(p.start),
        processorhelper.WithShutdown(p.shutdown),
    )
}
```

## processorhelper Process Function Signatures

```go
type ProcessTracesFunc  func(context.Context, ptrace.Traces) (ptrace.Traces, error)
type ProcessMetricsFunc func(context.Context, pmetric.Metrics) (pmetric.Metrics, error)
type ProcessLogsFunc    func(context.Context, plog.Logs) (plog.Logs, error)
```

Return the modified data; the helper forwards it to the next consumer.

## Create Function Signatures (raw, without helper)

```go
type CreateTracesFunc  func(context.Context, Settings, component.Config, consumer.Traces) (Traces, error)
type CreateMetricsFunc func(context.Context, Settings, component.Config, consumer.Metrics) (Metrics, error)
type CreateLogsFunc    func(context.Context, Settings, component.Config, consumer.Logs) (Logs, error)
```

## Processor Interfaces

```go
type Traces  interface { component.Component; consumer.Traces }
type Metrics interface { component.Component; consumer.Metrics }
type Logs    interface { component.Component; consumer.Logs }
```

## Implementation Pattern

```go
package myprocessor

import (
    "context"

    "go.opentelemetry.io/collector/pdata/plog"
    "go.uber.org/zap"
)

type myProcessor struct {
    cfg    *Config
    logger *zap.Logger
}

func newProcessor(cfg *Config, logger *zap.Logger) (*myProcessor, error) {
    return &myProcessor{cfg: cfg, logger: logger}, nil
}

func (p *myProcessor) start(_ context.Context, _ component.Host) error {
    return nil
}

func (p *myProcessor) shutdown(_ context.Context) error {
    return nil
}

func (p *myProcessor) processLogs(_ context.Context, ld plog.Logs) (plog.Logs, error) {
    // Transform ld in place or create new
    return ld, nil
}
```

## metadata.yaml

```yaml
type: myprocessor
status:
  class: processor
  stability:
    alpha: [traces, metrics, logs]
  distributions: [contrib]
  codeowners:
    active: [githubuser]
tests:
  config:
```
