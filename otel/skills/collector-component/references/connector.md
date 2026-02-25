# Connector Component

Import: `go.opentelemetry.io/collector/connector`

Connectors bridge two pipelines, acting as both exporter (consuming from one pipeline) and
receiver (producing into another). They can convert between signal types, enabling up to 9
combinations (traces/metrics/logs x traces/metrics/logs).

## Factory

```go
package myconnector

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/connector"
    "go.opentelemetry.io/collector/consumer"

    "github.com/org/repo/connector/myconnector/internal/metadata"
)

func NewFactory() connector.Factory {
    return connector.NewFactory(
        metadata.Type,
        createDefaultConfig,
        connector.WithTracesToMetrics(createTracesToMetrics, metadata.TracesToMetricsStability),
    )
}

func createDefaultConfig() component.Config {
    return &Config{}
}

func createTracesToMetrics(
    _ context.Context,
    params connector.Settings,
    cfg component.Config,
    nextConsumer consumer.Metrics,
) (connector.Traces, error) {
    c, err := newConnector(params, cfg.(*Config))
    if err != nil {
        return nil, err
    }
    c.metricsConsumer = nextConsumer
    return c, nil
}
```

## All 9 Factory Options

```go
connector.WithTracesToTraces(f, stability)
connector.WithTracesToMetrics(f, stability)
connector.WithTracesToLogs(f, stability)
connector.WithMetricsToTraces(f, stability)
connector.WithMetricsToMetrics(f, stability)
connector.WithMetricsToLogs(f, stability)
connector.WithLogsToTraces(f, stability)
connector.WithLogsToMetrics(f, stability)
connector.WithLogsToLogs(f, stability)
```

## Create Function Pattern

Each create function consumes one signal type and receives the next consumer for a
(potentially different) signal type:

```go
// Consumes traces, outputs metrics
type CreateTracesToMetricsFunc func(
    context.Context, Settings, component.Config, consumer.Metrics,
) (Traces, error)
```

The return type matches the INPUT signal (what the connector consumes from the pipeline).
The `consumer` parameter matches the OUTPUT signal (what it produces into the next pipeline).

## Connector Interfaces

```go
type Traces  interface { component.Component; consumer.Traces }
type Metrics interface { component.Component; consumer.Metrics }
type Logs    interface { component.Component; consumer.Logs }
```

## Implementation Pattern

```go
package myconnector

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/connector"
    "go.opentelemetry.io/collector/consumer"
    "go.opentelemetry.io/collector/pdata/pmetric"
    "go.opentelemetry.io/collector/pdata/ptrace"
    "go.uber.org/zap"
)

type myConn struct {
    cfg             *Config
    logger          *zap.Logger
    metricsConsumer consumer.Metrics
}

func newConnector(set connector.Settings, cfg *Config) (*myConn, error) {
    return &myConn{cfg: cfg, logger: set.Logger}, nil
}

func (c *myConn) Start(_ context.Context, _ component.Host) error {
    return nil
}

func (c *myConn) Shutdown(_ context.Context) error {
    return nil
}

func (c *myConn) Capabilities() consumer.Capabilities {
    return consumer.Capabilities{MutatesData: false}
}

// ConsumeTraces: this connector consumes traces and produces metrics
func (c *myConn) ConsumeTraces(ctx context.Context, td ptrace.Traces) error {
    metrics := c.convertTracesToMetrics(td)
    return c.metricsConsumer.ConsumeMetrics(ctx, metrics)
}

func (c *myConn) convertTracesToMetrics(td ptrace.Traces) pmetric.Metrics {
    md := pmetric.NewMetrics()
    // Build metrics from trace data
    return md
}
```

## metadata.yaml

Stability uses `input_to_output` format:

```yaml
type: myconnector
status:
  class: connector
  stability:
    alpha: [traces_to_metrics]
  distributions: [contrib]
  codeowners:
    active: [githubuser]
tests:
  config:
```

Generated constants use combined naming: `TracesToMetricsStability`.
