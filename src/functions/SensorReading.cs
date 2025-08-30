
namespace IngestionFn;

public record SensorReading(
    string DeviceId,
    System.DateTime Timestamp,
    double TemperatureC,
    double HumidityPct
);
