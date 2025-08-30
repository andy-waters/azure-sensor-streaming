
# azure-sensor-streaming

*** azure-sensor-streaming ***  is an end-to-end reference for real-time data engineering on Azure. It streams temperature and humidity readings into Azure Event Hubs, processes them with Azure Functions (.NET 8), stores curated records in Azure SQL, and exposes query endpoints through a .NET 8 Minimal API (optionally fronted by API Management). The project is production-shaped—Bicep for infrastructure, Azure DevOps multi-stage pipelines for CI/CD, Key Vault for secrets, and Application Insights for observability—while remaining easy to run locally via a shared devcontainer, Azurite, and Azure SQL Edge.

## Event schema
```json
{
  "deviceId": "sensor-001",
  "timestamp": "2025-08-30T10:15:00Z",
  "temperatureC": 22.7,
  "humidityPct": 56.4
}
```

## Quickstart
1. Open in VS Code and **Reopen in Container** when prompted.
2. Start local services:
   ```bash
   docker compose up -d
   ```
3. Run API:
   ```bash
   cd src/api
   dotnet run
   ```
4. Run Functions:
   ```bash
   cd ../functions
   func start
   ```

### Health checks
- API: `GET /health`
- Functions: `GET /api/Ping`

## Structure
- `src/api` – .NET 8 Minimal API (serving)
- `src/functions` – Azure Functions (.NET 8 isolated): HTTP ping + Event Hub trigger (`SensorIngest`)
- `infra` – Bicep IaC (KV, App Insights, Storage, Event Hubs, SQL, App Service, Function App)
- `.ado` – Azure DevOps CI/CD pipelines & templates
- `tests` – xUnit sample + k6 perf test
- `.devcontainer` – reproducible environment
