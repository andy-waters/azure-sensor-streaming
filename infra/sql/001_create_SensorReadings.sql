
-- infra/sql/001_create_SensorReadings.sql
CREATE TABLE IF NOT EXISTS SensorReadings (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    DeviceId NVARCHAR(100) NOT NULL,
    [Timestamp] DATETIME2 NOT NULL,
    TemperatureC FLOAT NOT NULL,
    HumidityPct FLOAT NOT NULL
);
GO

CREATE INDEX IF NOT EXISTS IX_SensorReadings_Timestamp ON SensorReadings([Timestamp]);
GO
