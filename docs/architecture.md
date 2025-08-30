
# Architecture

```mermaid
flowchart LR
    subgraph Ingestion
      S[IoT Sensor(s)] -->|temp+humidity JSON| EH[(Azure Event Hubs)]
      EH --> F[Azure Function - SensorIngest]
      F --> ST[(Azure Storage - staging)]
      F --> SQL[(Azure SQL - curated)]
    end

    subgraph Serving
      API[.NET 8 Minimal API] --> SQL
      API -- metrics --> AI[App Insights]
      API --> APIM[API Management]
    end

    subgraph Sec & Mgmt
      KV[Key Vault]
      MON[Azure Monitor/Alerts]
    end

    KV --> API
    KV --> F
    API --> MON
    F --> MON
```

## Non-functional goals
- p95 latency < 300ms for read API
- At-least-once processing from Event Hubs
- Observability as code (dashboards + alerts deployed via Bicep)
- Slot-based or blue/green deploys for API/Functions
