# ReFrontend

This is a self-customizing UI project that dynamically re-styles itself based on user prompts. It uses OpenAI's API to generate CSS styles.

## Features
- Dynamically update themes and styles based on user input.
- Predefined prompts for quick theme changes.
- "New Chat" button to reset the UI to default settings.

## Demo

![UI Demo](assets/testvid1.gif)
![UI Demo](assets/testvid3.gif)


## Setup Instructions

### Backend Setup
1. Navigate to the `backend` folder:
```
cd backend
```

2. Create a .env file in the backend folder and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

3. Create a virtual environment:
```
python3 -m venv ai-ui-env
source ai-ui-env/bin/activate # For MacOS/Linux
ai-ui-env\Scripts\activate # For Windows
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Run the Flask server:
```
python app.py
```

### Frontend Setup
1. Navigate to the `frontend` folder:
```
cd frontend
```

2. Open `index.html` in your browser.

### Example Prompts
- "Make it glow-in-the-dark"
- "Make it superhero themed"
- "Make it night mode"
