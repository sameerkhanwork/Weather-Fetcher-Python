#!/usr/bin/env python3
"""
Weather Data Fetcher

This script fetches weather data from the Open-Meteo API & formats it as a Markdown table.
"""

import requests
import json
from typing import Dict, Any
from tabulate import tabulate


def fetch_weather_data(api_url: str) -> Dict[str, Any]:
    """
    Fetch weather data from the Open-Meteo API.
    
    Args:
        api_url (str): The API endpoint URL
        
    Returns:
        Dict[str, Any]: Weather data from the API
        
    Raises:
        requests.RequestException: If the API request fails
    """
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        # Use json.loads() for API response parsing as required
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to fetch weather data: {e}")


def format_weather_as_markdown(weather_data: Dict[str, Any]) -> str:
    """
    Format weather data as a Markdown table using tabulate library.
    
    Args:
        weather_data (Dict[str, Any]): Weather data from the API
        
    Returns:
        str: Formatted Markdown table
    """
    # Extract current weather data
    current_weather = weather_data.get('current_weather', {})
    
    # Get temperature and wind speed
    temperature = current_weather.get('temperature', 'N/A')
    wind_speed = current_weather.get('windspeed', 'N/A')
    
    # Get weather condition (Open-Meteo uses weathercode, we'll map it to readable text)
    weather_code = current_weather.get('weathercode', 0)
    condition = get_weather_condition(weather_code)
    
    # Prepare data for tabulate
    table_data = [
        ["Temperature (°C)", temperature],
        ["Wind Speed (km/h)", wind_speed],
        ["Condition", condition]
    ]
    
    # Use tabulate library for table formatting as required
    markdown_table = tabulate(table_data, headers=["Metric", "Value"], tablefmt="pipe")
    
    return markdown_table


def get_weather_condition(weather_code: int) -> str:
    """
    Convert weather code to human-readable condition.
    
    Args:
        weather_code (int): Weather code from Open-Meteo API
        
    Returns:
        str: Human-readable weather condition
    """
    # Open-Meteo weather codes mapping
    weather_conditions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Slight Hail",
        99: "Thunderstorm with Heavy Hail"
    }
    
    return weather_conditions.get(weather_code, "Unknown")


def main():
    """Main function to fetch and display weather data."""
    # API endpoint for London coordinates
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
    
    try:
        print("Fetching weather data...")
        weather_data = fetch_weather_data(api_url)
        
        print("\nWeather Data (Raw JSON):")
        print(json.dumps(weather_data, indent=2))
        
        print("\n" + "="*50)
        print("FORMATTED WEATHER DATA (Markdown Table):")
        print("="*50)
        
        markdown_table = format_weather_as_markdown(weather_data)
        print(markdown_table)
        
        # Save to file
        with open("weather_report.md", "w", encoding="utf-8") as f:
            f.write("# Weather Report\n\n")
            f.write(markdown_table)
        
        print(f"\nWeather report saved to 'weather_report.md'")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
