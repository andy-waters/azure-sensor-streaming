
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

// TODO: replace with real SQL queries
app.MapGet("/readings/sample", () => Results.Ok(new {
    deviceId = "sensor-001",
    timestamp = DateTime.UtcNow,
    temperatureC = 22.7,
    humidityPct = 56.4
}));

app.Run();
