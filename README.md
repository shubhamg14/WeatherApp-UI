# WeatherApp-UI
UI to fetch and display data using WeatherApp-API (API functionality can be found @https://github.com/shubhamg14/WeatherApp-API

This implementation of an UI follows a dynamic approach that uses asynchronous JavaScript requests to send the user-inputted data to the REST API(WeatherApp-API - @https://github.com/shubhamg14/WeatherApp-API) , receive the structured results, and then publish them into the page without refreshing the whole page again.

This Webpage takes an input date and then plot the Forecasts TMIN, TMAX for next five days.

## The UI has the following functionality:

**_Historical_** - Enter a date from 1st January'2013 - 28th March'2019 and you will get the minimum and maximum temperature for that day.

**_Forecast_** - Enter any existing and future date and you will get a weather forecast in a table format as well as a line graph.
The Forecast may not be accurate as it is calculated by taking the running average of temeperature for past 365 days.

**_OpenWeather_** - This page displays the weather forecast for next 5 days which is fetched from a third party API (Openweathemap.com).
This page outputs the forecast in a table format as well as graph.

## Following packages are required to run this code base:

