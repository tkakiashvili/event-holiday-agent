# 🎉 Event & Holiday Organizer Agent

An AI-powered Practical Assistant Agent built with **LangGraph** and **ChatGroq** that helps users organize events, check official public holidays, verify current weather conditions, and manage a guest list with human-in-the-loop approval before removing guests.

## Features & Tools
- **`get_public_holidays`**: Fetches official public holidays by country code and year using the [Nager.Date API](https://date.nager.at/).
- **`get_city_weather`**: Checks real-time temperature and wind speed using the [Open-Meteo API](https://open-meteo.com/).
- **`add_guest` / `list_guests`**: Manages the event guest list in conversation memory (`InMemorySaver`).
- **`remove_guest` (Human Approval)**: Uses LangGraph `interrupt()` to pause and ask for user confirmation before deleting any guest.

## Setup & Installation

1. Clone this repository and install dependencies:
```bash
pip install -r requirements.txt
https://event-holiday-agent-usbm8rlz63mwzy6lmvtsrh.streamlit.app/https://event-holiday-agent-usbm8rlz63mwzy6lmvtsrh.streamlit.app/
