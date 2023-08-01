# WhatsApp Chat Analyzer


WhatsApp Chat Analyzer is a Python-based web application built with Streamlit that provides insightful analytics on a WhatsApp chat. By uploading the exported chat file from WhatsApp, users can explore various statistics and visualizations, including the most active users, busiest hours of the day, most frequent words, and busiest days. The project uses popular Python libraries such as Pandas, NumPy, Matplotlib, Seaborn, and urlextract to create stunning visual representations of the chat analysis.
## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
## Getting Started

To use the WhatsApp Chat Analyzer, follow these instructions:

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.x installed on your system.
3. Install the required Python packages by running the following command:

```bash
pip install -r requirements.txt
```
```bash
streamlit run main.py
```
## Usage

1. Export your WhatsApp chat by following these steps:
   - Open the WhatsApp chat you want to analyze.
   - Click on the three-dot menu on the top-right corner.
   - Select "More" > "Export Chat."
   - Choose "Without Media" to export the chat without media files.
   - Save the exported file (.txt) to your computer.

2. Start the Streamlit app by running the following command:

```bash
streamlit run main.py
```
## Features

The WhatsApp Chat Analyzer offers the following features:

- Most active users: Displays a bar chart showing the number of messages sent by each participant in the chat.
- Busiest hours of the day: Presents a line chart indicating the number of messages sent per hour.
- Most frequent words: Shows a word cloud of the most frequently used words in the chat.
- Busiest days: Displays a bar chart showing the number of messages sent on each day of the week.

