# Extension Component

Import: `go.opentelemetry.io/collector/extension`

Extensions provide capabilities that are not part of the data pipeline (health checks,
service discovery, etc.). They are the simplest component type.

**Key difference**: `NewFactory` takes positional arguments, NOT variadic options.

## Factory

```go
package myextension

import (
    "context"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/extension"

    "github.com/org/repo/extension/myextension/internal/metadata"
)

// NOTE: Positional args, no WithTraces/WithMetrics/WithLogs options
func NewFactory() extension.Factory {
    return extension.NewFactory(
        metadata.Type,
        createDefaultConfig,
        createExtension,
        metadata.ExtensionStability,
    )
}

func createDefaultConfig() component.Config {
    return &Config{
        Endpoint: "localhost:13133",
    }
}

func createExtension(
    _ context.Context,
    set extension.Settings,
    cfg component.Config,
) (extension.Extension, error) {
    return newExtension(cfg.(*Config), set), nil
}
```

## Create Function Signature

```go
type CreateFunc func(context.Context, Settings, component.Config) (Extension, error)
```

No consumer parameter; extensions are not part of the data pipeline.

## Extension Interface

```go
type Extension interface {
    component.Component  // Start + Shutdown only
}
```

## Optional Interfaces

Extensions can implement additional interfaces for extra capabilities:

```go
// PipelineWatcher: notified when pipelines are ready/not ready
type PipelineWatcher interface {
    Ready() error
    NotReady() error
}

// Dependent: declares dependencies on other extensions
type Dependent interface {
    Dependencies() []component.ID
}
```

## Implementation Pattern

```go
package myextension

import (
    "context"
    "net/http"

    "go.opentelemetry.io/collector/component"
    "go.opentelemetry.io/collector/extension"
    "go.uber.org/zap"
)

type myExt struct {
    cfg    *Config
    logger *zap.Logger
    server *http.Server
}

func newExtension(cfg *Config, set extension.Settings) *myExt {
    return &myExt{cfg: cfg, logger: set.Logger}
}

func (e *myExt) Start(_ context.Context, _ component.Host) error {
    e.server = &http.Server{Addr: e.cfg.Endpoint}
    go func() { _ = e.server.ListenAndServe() }()
    return nil
}

func (e *myExt) Shutdown(ctx context.Context) error {
    if e.server != nil {
        return e.server.Shutdown(ctx)
    }
    return nil
}
```

## metadata.yaml

Uses `extension` (not signal types) for stability:

```yaml
type: myextension
status:
  class: extension
  stability:
    alpha: [extension]
  distributions: [contrib]
  codeowners:
    active: [githubuser]
tests:
  config:
    endpoint: localhost:0
```

Generated constant: `ExtensionStability`.
