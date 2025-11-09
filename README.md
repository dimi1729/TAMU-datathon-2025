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
*   **Classes:** Access information about courses, degree plans, and registration.
*   **Events:** Stay up-to-date on campus events, workshops, and social gatherings.
*   **Student Organizations:** Discover and learn about student clubs and organizations.

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


**Q**: What was the score of the last LSU game?
**A**: LSU's most recent game was against Alabama at Bryant-Denny Stadium. The final score was:
Alabama 20, LSU 9

The Tigers fell to the Crimson Tide in this matchup. Would you like me to check any other information about LSU's season?

### Actions

*   **Google Calendar Integration:** Add events, deadlines, and reminders directly to your Google Calendar.
*   **Email Composition:** Draft and send emails to professors, student organizations, or other contacts.


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
