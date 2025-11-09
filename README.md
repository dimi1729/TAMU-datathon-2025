# TAMU Datathon 2025: College Assistant Chatbot

This repository contains the code for a chatbot created for the TAMU Datathon 2025 MCP Challenge. The chatbot is designed to assist Texas A&M University students by providing information and performing actions related to various aspects of college life.

## Project Overview

The goal of this project is to create a valuable tool for college students by leveraging our MCP. The chatbot serves as a centralized source of information, answering questions and executing tasks to help students navigate their lives at the university.

The project is hosted at campuscompass.wiki

## Features

The chatbot can provide information and perform actions in the following areas:

### Information Retrieval

*   **Sports:** Get information about college sports teams, schedules, and results.
*   **Food:** Find out about on-campus and off-campus dining options, hours, and menus.
*   **Apartments:** Get details on housing options, including availability, pricing, and amenities.
*   **Events:** Stay up-to-date on campus events, workshops, and social gatherings.
*   **Weather** Plan what you will wear to campus based on the live weather information. 

Examples of questions to ask:
**Q**: What events are happening at Texas A&M
**A**: Here are the upcoming events in and around Texas A&M:

Immediate upcoming events:
1. Tomorrow (Nov 9): Campus Nights Tour with Josiah Queen, Hulvey, and Claire Leslie at Rudder Auditorium
2. Nov 14: TAMU Men's Basketball vs. UCF Knights at Reed Arena
3. Nov 15: TAMU Football vs. South Carolina Gamecocks at Kyle Field
4. Nov 18: TAMU Men's Basketball vs. Montana Grizzlies at Reed Arena
5. Nov 21: TAMU Men's Basketball vs. Manhattan Jaspers at Reed Arena
6. Nov 22: TAMU Football vs. Samford University Bulldogs at Kyle Field
7. Nov 25: TAMU Men's Basketball vs. Mississippi Valley State at Reed Arena

There are also numerous basketball games scheduled through March 2026, including matchups against traditional rivals like Texas Longhorns (Feb 28, 2026) and other SEC opponents.

Most events are taking place at three main venues:
- Kyle Field (Football games)
- Reed Arena (Basketball games)
- Rudder Auditorium (Concerts/Shows)

Would you like me to provide more specific details about any of these events or help you search for additional information?


**Q**: Can you add my 12:30 chemistry class on MWF to my calendar?
**A**: I've created the event with the following details:
- Title: Chemistry Class
- Date: Monday, November 10, 2025
- Start Time: 12:30 PM
- End Time: 1:20 PM (assuming a standard 50-minute class period)

If you'd like to add more details like the classroom location or any specific notes, just let me know and I can create a new event with that additional information.


**Q**: What was the score in this week's aggies game?
**Context**: The chatbot figures out who Aggies are and checked the ESPN api for the score data.
**A**: Texas A&M defeated Missouri 38-17 in their most recent game. The game was played at Memorial Stadium and is now final.

**Q**: What's the weather like around Texas A&M's campus?
**Context**: The chatbot figures out where Texas A&M's campus is and then uses that infromation to check the current weather using an Open-Meteo API.
**A**: Currently in College Station, it's 16.8°C (about 62°F) with a light wind speed of 25.6 km/h (about 16 mph) coming from a northerly direction. The weather code indicates partly cloudy conditions. It's a fairly mild day, typical for a fall day in central Texas. This is pretty comfortable weather for walking around campus or spending time outdoors!

Would you like me to check anything else about the area, such as local events or deals near campus?

**Q**: I am a little hungry. Are there any good food deals in College Station area?
**Context**: The chatbot uses Discount API, which keeps track of good discounts and promotions. It uses it to craft a response about deals in College Station area. 
**A**: I found several restaurant deals in College Station! Here are the current offers:

1. La Botana Mexican Restaurant
- $25 value for $10 (60% off)
- Minimum purchase of $50
- Traditional Mexican and Tex-Mex food

2. Hot Dogs & Wings Etc
- $5 value for $2 (60% off)
- Minimum purchase of $10
- Known for generous portions at moderate prices

3. Luigi's Patio Ristorante
- $10 value for $4 (60% off)
- Minimum purchase of $20
- Valid for dinner only
- Authentic Italian cuisine with pasta, seafood, chicken, and veal dishes
- Features outdoor patio dining and live music

4. Porters Dining & Butcher
- $15 value for $6 (60% off)
- Minimum purchase of $30
- Valid for lunch only (not valid Saturday and Sunday)
- Upscale dining with wood-fired flavors and seasonal menu

5. Pin-Toh Thai Cafe
- $15 value for $6 (60% off)
- Minimum purchase of $30
- Thai cuisine

6. West End Elixir Co
- $25 value for $10 (60% off)
- Minimum purchase of $50
- Features brick oven-fired pizzas and cocktails

7. C & A's Kitchen
- $15 value for $6 (60% off)
- Minimum purchase of $30

These deals offer a good variety of cuisines - Mexican, Italian, Thai, American, and more. The best value for a smaller purchase might be Hot Dogs & Wings Etc, where you only need a $10 minimum purchase to use the deal. For a nicer dining experience, Luigi's Patio Ristorante or Porters Dining & Butcher both offer good savings on quality meals.

**Q**: I have a budget of $800. Are there any good apartments for me in College Station area?
**Context**: The chatbot uses Zillow's api to learn about rentals in the area and then filters them using the requirements from the user.
**A**: Good news! I found some rental options in College Station that are within your $800 budget. Here are the most relevant options:

1. 601 Luther St W (Apartment)
- Price: $709/month
- 2 bed, 2 bath
- 862 sq ft

2. 1806 Yellowhouse Cir (Apartment)
- Price: $730/month
- 1 bed, 1 bath
- 600 sq ft

Both of these options are within your budget of $800. The Luther Street apartment offers more space and an extra bedroom and bathroom for just $709, which could be a great value. The Yellowhouse Circle apartment is slightly more expensive at $730 but might be perfect if you're looking for a one-bedroom setup.

Would you like me to help you get more specific information about either of these properties or would you like to see what else might be available in different areas of College Station? I can also help you check what the weather is like in that area or look for local events if you're planning to visit these properties.

### Actions

*   **Google Calendar Integration:** Add events, deadlines, and reminders directly to your Google Calendar.


## Tech Stack

*   **Frontend:** Next.js, React, TypeScript, Tailwind CSS
*   **Backend:** Python, Flask
*   **Deployment:** Vercel (frontend), Railway (backend)

## Getting Started

The project is hosted at campuscompass.wiki. However, to get a local copy up and running, follow these steps:

### Prerequisites

*   Node.js and npm
*   Python 3.x
*   `uv` or `pip`

### Installation

1.  **Clone the repo:**
    ```sh
    git clone https://github.com/your_username/TAMU-datathon-2025.git
    cd TAMU-datathon-2025
    ```

2.  **Set up the backend:**
    ```sh
    cd api
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

3.  **Set up the frontend:**
    ```sh
    cd ../website/frontend
    npm install
    ```

4. **Run the server:**
    (In the website directory)
    On Mac/linux: `./start-dev.sh`
    On Windows: `./start-dev.bat`

5. **View result in browser**
  Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## API

The backend API is built with Flask and provides the following endpoints:

*   `POST /api/chat`: The main endpoint for interacting with the chatbot. It receives a message from the user and returns a response from the bot.
