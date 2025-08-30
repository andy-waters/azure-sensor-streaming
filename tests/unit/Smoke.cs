
using Xunit;
using FluentAssertions;

namespace Api.Tests;

public class Smoke
{
    [Fact]
    public void Basic_math()
    {
        (1 + 1).Should().Be(2);
    }
}
