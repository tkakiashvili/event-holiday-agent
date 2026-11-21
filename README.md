# 🎉 Event & Holiday Organizer Agent

## Overview & Purpose
**Event & Holiday Organizer Agent** is a practical AI assistant designed to help users plan events, check official public holidays, verify real-time weather conditions, and manage an event guest list safely. Built using **LangGraph** and **Groq** (`openai/gpt-oss-120b`), the agent combines conversational memory, external API integrations, and a human-in-the-loop approval mechanism for destructive actions.

## Architecture & Workflow
The agent is structured as a stateful **LangGraph (`StateGraph`)** workflow:
1. **Assistant Node:** Processes user queries using `ChatGroq` bound to 5 custom tools, guided by a system prompt that enforces direct tool execution.
2. **Conditional Routing (`tools_condition`):** Automatically decides whether to invoke a tool or respond directly to the user.
3. **Tool Node (`ToolNode`):** Executes external API calls or guest list operations and returns structured results back to the assistant.
4. **Memory (`InMemorySaver`):** Maintains conversation context and guest list state across multi-turn interactions within a session.

## Implemented Tools
- **`get_public_holidays(country_code, year)`**: Connects to the **Nager.Date API** to retrieve official public holidays for a specified country and year.
- **`get_city_weather(latitude, longitude)`**: Connects to the **Open-Meteo API** to fetch live temperature and wind speed data.
- **`add_guest(name)`**: Adds a guest to the event guest list while preventing duplicate entries.
- **`list_guests()`**: Retrieves all guests currently stored in the session list.
- **`remove_guest(name)` (Human-in-the-Loop)**: Uses LangGraph's `interrupt()` function to pause execution before deleting a guest. The deletion proceeds only upon explicit user approval (`Yes` / `True`); otherwise, the action is cancelled and the list remains unchanged.

## Interfaces & Deployment
- **Jupyter Notebook (`AI Agent.ipynb`)**: Contains the full implementation, state graph diagram, 7 isolated test cases with execution trajectories, and an evaluation table.
- **Web Interface (`app.py`)**: Interactive chat interface built with **Streamlit**, featuring visual confirmation buttons for destructive actions.
- **Command-Line Interface (`main.py`)**: Terminal-based interactive loop supporting real-time human approval prompts.

## Live Demo
- [Streamlit Web App](https://event-holiday-agent-usbm8rlz63mwzy6lmvtsrh.streamlit.app/)

## Setup & Installation
1. Install required dependencies:
```bash
pip install -r requirements.txt
# 🎉 Event & Holiday Organizer Agent (ღონისძიებებისა და უქმე დღეების ორგანიზატორი აგენტი)

## მიმოხილვა და დანიშნულება
**Event & Holiday Organizer Agent** არის პრაქტიკული AI ასისტენტი, რომელიც მომხმარებელს ეხმარება ღონისძიებების დაგეგმვაში, ოფიციალური უქმე დღეების შემოწმებაში, რეალურ დროში ამინდის პროგნოზის ნახვასა და სტუმრების სიის უსაფრთხოდ მართვაში. აგენტი აგებულია **LangGraph** ფრეიმვორკისა და **Groq** (`openai/gpt-oss-120b`) მოდელის გამოყენებით და აერთიანებს საუბრის მეხსიერებას, გარე API სერვისებსა და მომხმარებლის დადასტურების (*Human-in-the-Loop*) მექანიზმს კრიტიკული მოქმედებებისთვის.

## არქიტექტურა და მუშაობის პრინციპი
აგენტი აწყობილია მდგომარეობაზე დაფუძნებული **LangGraph (`StateGraph`)** სტრუქტურით:
1. **Assistant კვანძი:** ამუშავებს მომხმარებლის მოთხოვნებს `ChatGroq` მოდელის საშუალებით, რომელთანაც დაკავშირებულია 5 სპეციალური ინსტრუმენტი (Tool) და სისტემური ინსტრუქცია (`SYSTEM_PROMPT`).
2. **პირობითი მარშრუტიზაცია (`tools_condition`):** ავტომატურად განსაზღვრავს, სჭირდება თუ არა აგენტს რომელიმე ინსტრუმენტის გამოძახება, თუ პირდაპირ უნდა უპასუხოს მომხმარებელს.
3. **ინსტრუმენტების კვანძი (`ToolNode`):** ასრულებს გარე API მოთხოვნებს ან სტუმრების სიის ოპერაციებს და მიღებულ შედეგს უბრუნებს ასისტენტს.
4. **მეხსიერება (`InMemorySaver`):** ინახავს დიალოგის კონტექსტსა და სტუმრების სიის მდგომარეობას სესიის განმავლობაში.

## შექმნილი ინსტრუმენტები (Tools)
- **`get_public_holidays(country_code, year)`**: უკავშირდება **Nager.Date API**-ს და მოაქვს ოფიციალური უქმე დღეების სია მითითებული ქვეყნისა და წლის მიხედვით.
- **`get_city_weather(latitude, longitude)`**: უკავშირდება **Open-Meteo API**-ს და გვაწვდის რეალურ დროში ტემპერატურასა და ქარის სიჩქარეს.
- **`add_guest(name)`**: ამატებს სტუმარს ღონისძიების სიაში და იცავს სიას დუბლიკატებისგან.
- **`list_guests()`**: აჩვენებს სესიის სიაში ამჟამად დამატებულ ყველა სტუმარს.
- **`remove_guest(name)` (Human-in-the-Loop)**: იყენებს LangGraph-ის `interrupt()` ფუნქციას, რათა სტუმრის წაშლამდე შეაჩეროს შესრულება და მოითხოვოს მომხმარებლის დადასტურება. წაშლა სრულდება მხოლოდ თანხმობის (`Yes` / `True`) შემდეგ; უარის შემთხვევაში მოქმედება უქმდება და სია უცვლელი რჩება.

## ინტერფეისები და გაშვება
- **Jupyter Notebook (`AI Agent.ipynb`)**: მოიცავს სრულ კოდს, გრაფის ვიზუალურ დიაგრამას, 7 იზოლირებულ ტესტს ტრაექტორიებითა და შეფასების ცხრილს.
- **ვებ-ინტერფეისი (`app.py`)**: **Streamlit**-ზე აწყობილი ინტერაქტიული ჩატი დადასტურების ღილაკებით კრიტიკული მოქმედებებისთვის.
- **ტერმინალის ვერსია (`main.py`)**: ტერმინალში (CLI) გასაშვები ინტერაქტიული რეჟიმი დადასტურების მოთხოვნით.

## ონლაინ დემო (Live Demo)
- [Streamlit Web App](https://event-holiday-agent-usbm8rlz63mwzy6lmvtsrh.streamlit.app/)

## დაყენება და გაშვება
1. საჭირო ბიბლიოთეკების ინსტალაცია:
```bash
pip install -r requirements.txt
