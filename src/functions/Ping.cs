
using System.Net;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

namespace IngestionFn;

public class Ping
{
    private readonly ILogger _logger;
    public Ping(ILoggerFactory loggerFactory) => _logger = loggerFactory.CreateLogger<Ping>();

    [Function("Ping")]
    public HttpResponseData Run([HttpTrigger(AuthorizationLevel.Anonymous, "get")] HttpRequestData req)
    {
        _logger.LogInformation("Ping triggered.");
        var res = req.CreateResponse(HttpStatusCode.OK);
        res.WriteString("{"status":"ok"}");
        res.Headers.Add("Content-Type", "application/json");
        return res;
    }
}
