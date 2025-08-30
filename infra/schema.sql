
-- SQL schema for sensor readings
CREATE TABLE SensorReadings (
    Id INT IDENTITY PRIMARY KEY,
    DeviceId NVARCHAR(100) NOT NULL,
    Timestamp DATETIME2 NOT NULL,
    TemperatureC FLOAT NOT NULL,
    HumidityPct FLOAT NOT NULL
);
