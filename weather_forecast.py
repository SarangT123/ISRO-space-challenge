import python_weather
import asyncio
import sys

async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client()

    # fetch a weather forecast from a city
    weather = await client.find(sys.argv[2])

    # returns the current day's forecast temperature (int)
    # get the weather forecast for a few days
    dates = ""
    weather_text = ""
    temp = ""
    for forecast in weather.forecasts:
        dates = f"{dates}#{str(forecast.date)}" 
        weather_text= f"{weather_text}#{str(forecast.sky_text)}"
        temp = f"{temp}#{forecast.temperature}"

    # close the wrapper once done
    await client.close()
    if sys.argv[1] == '0': print(dates)
    if sys.argv[1] == '1': print(temp)
    if sys.argv[1] == '2': print(weather_text)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())