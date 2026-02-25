# Exporter Component

Import: `go.opentelemetry.io/collector/exporter`

Exporters are terminal: they send data out and have NO next consumer parameter.
Use `exporterhelper` for retry, queue, timeout, and observability.

## Factory

```go
package myexporter

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/exporter"
    "go.opentelemetry.io/collector/exporter/exporterhelper"
    "go.opentelemetry.io/collector/config/configretry"

    "github.com/org/repo/exporter/myexporter/internal/metadata"
)

func NewFactory() exporter.Factory {
    return exporter.NewFactory(
        metadata.Type,
        createDefaultConfig,
        exporter.WithTraces(createTracesExporter, metadata.TracesStability),
        exporter.WithMetrics(createMetricsExporter, metadata.MetricsStability),
        exporter.WithLogs(createLogsExporter, metadata.LogsStability),
    )
}

func createDefaultConfig() component.Config {
    return &Config{
        TimeoutConfig: exporterhelper.NewDefaultTimeoutConfig(),
        BackOffConfig: configretry.NewDefaultBackOffConfig(),
    }
}

func createLogsExporter(
    ctx context.Context,
    set exporter.Settings,
    cfg component.Config,
) (exporter.Logs, error) {
    oCfg := cfg.(*Config)
    exp, err := newExporter(oCfg, set)
    if err != nil {
        return nil, err
    }
    return exporterhelper.NewLogs(
        ctx, set, cfg,
        exp.pushLogs,
        exporterhelper.WithStart(exp.start),
        exporterhelper.WithShutdown(exp.shutdown),
        exporterhelper.WithTimeout(oCfg.TimeoutConfig),
        exporterhelper.WithRetry(oCfg.BackOffConfig),
    )
}
```

## Create Function Signatures (No Next Consumer)

```go
type CreateTracesFunc  func(context.Context, Settings, component.Config) (Traces, error)
type CreateMetricsFunc func(context.Context, Settings, component.Config) (Metrics, error)
type CreateLogsFunc    func(context.Context, Settings, component.Config) (Logs, error)
```

## exporterhelper Push Function Signatures

```go
// These are what you provide to exporterhelper.NewTraces/NewMetrics/NewLogs
type ConsumeTracesFunc  func(context.Context, ptrace.Traces) error
type ConsumeMetricsFunc func(context.Context, pmetric.Metrics) error
type ConsumeLogsFunc    func(context.Context, plog.Logs) error
```

## exporterhelper Options

```go
exporterhelper.WithStart(func(context.Context, component.Host) error)
exporterhelper.WithShutdown(func(context.Context) error)
exporterhelper.WithTimeout(exporterhelper.TimeoutConfig{Timeout: 5 * time.Second})
exporterhelper.WithRetry(configretry.NewDefaultBackOffConfig())
exporterhelper.WithCapabilities(consumer.Capabilities{MutatesData: false})
exporterhelper.WithQueue(exporterhelper.QueueConfig{...})
```

## Config Pattern

```go
package myexporter

import (
    "go.opentelemetry.io/collector/config/configretry"
    "go.opentelemetry.io/collector/exporter/exporterhelper"
)

type Config struct {
    exporterhelper.TimeoutConfig `mapstructure:",squash"`
    configretry.BackOffConfig    `mapstructure:"retry_on_failure"`

    Endpoint string `mapstructure:"endpoint"`
}
```

## Implementation Pattern

```go
package myexporter

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/exporter"
    "go.opentelemetry.io/collector/pdata/plog"
    "go.uber.org/zap"
)

type logsExporter struct {
    cfg    *Config
    logger *zap.Logger
}

func newExporter(cfg *Config, set exporter.Settings) (*logsExporter, error) {
    return &logsExporter{cfg: cfg, logger: set.Logger}, nil
}

func (e *logsExporter) start(_ context.Context, _ component.Host) error {
    // Initialize clients/connections
    return nil
}

func (e *logsExporter) shutdown(_ context.Context) error {
    // Close clients/connections
    return nil
}

func (e *logsExporter) pushLogs(_ context.Context, ld plog.Logs) error {
    // Send data to external system
    return nil
}
```

## metadata.yaml

```yaml
type: myexporter
status:
  class: exporter
  stability:
    beta: [traces, metrics, logs]
  distributions: [contrib]
  codeowners:
    active: [githubuser]
tests:
  config:
    endpoint: localhost:0
```
