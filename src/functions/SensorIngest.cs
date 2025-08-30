
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace IngestionFn;

public class SensorIngest
{
    private readonly ILogger _logger;
    public SensorIngest(ILoggerFactory loggerFactory) => _logger = loggerFactory.CreateLogger<SensorIngest>();

    [Function("SensorIngest")]
    public void Run([EventHubTrigger("events", Connection = "EventHubs:ConnectionString")] string[] events)
    {
        foreach (var payload in events)
        {
            try
            {
                var reading = JsonSerializer.Deserialize<SensorReading>(payload);
                if (reading is null)
                {
                    _logger.LogWarning("Null reading payload: {payload}", payload);
                    continue;
                }

                _logger.LogInformation("Device={DeviceId} Time={Timestamp:o} TempC={Temp} Humidity%={Humidity}",
                    reading.DeviceId, reading.Timestamp, reading.TemperatureC, reading.HumidityPct);

                // TODO: save to SQL (via Dapper/EF Core)
            }
            catch (System.Exception ex)
            {
                _logger.LogError(ex, "Failed to process payload: {payload}", payload);
            }
        }
    }
}
