from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import re
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)  # Finds the first JSON-like block
    if match:
        return match.group(0)  # Return the extracted JSON part
    return None
@app.route("/generate-styles", methods=["POST"])
def generate_styles():
    try:
        user_prompt = request.json.get("userPrompt", "")
        system_prompt = """Generate valid CSS styles based on user preferences. 

        - Your response must be a **valid JSON object** containing CSS styles.
        - Do **not** include explanations, markdown formatting, or any additional text.
        - Property names must be **camelCase**.
        - Always return styles for the following elements (unless user mentions change of size):
          - The `body` (include background color, font, and style even if not explicitly requested)
          - The `.chat-box` (always include border, boxShadow, backgroundColor, and borderRadius)
          - The `.button` (always include color, backgroundColor, borderColor, and boxShadow)
          - The `.header h1` (always include fontSize and color)
          - The `.chat-input` (always include fontSize and color)
        - Reset any previous boxShadow or border properties when a new prompt is given.
        - **Do NOT modify the size (`width`, `height`, `padding`, etc.) of elements unless the user explicitly 
            mentions size changes (keywords: big, bigger, small, smaller, wider, taller, etc)**.
        - **Do NOT include pseudo-classes like `:hover`, `:focus`, `:active`, `:before`, or `:after`.**
        - **Whenever you return any color properties, don't forget to apply it to the `.header h1` and the borders**
        - Adapt to **different moods and themes**:
          - "Make it blue" → Use shades of blue 
          - "Make it romantic" → Use soft pinks, elegant fonts, and rounded corners
          - "Make it futuristic" → Use neon colors, bold fonts, and sleek borders
          - "Make it night mode" → Use dark colors, contrasting font colors
        - Adapt to **size changes**:
          - "Make it big" → Increase both the height and max-width of the `.chat-box`
          - "Make it small" → Decrease both the height and max-width of the `.chat-box`
          - "Make the font big" → Increase font size of `.chat-input`
          - "Make the font small" → Decrease font size of `.chat-input`

        Return only a **JSON object** with CSS properties and no pseudo-classes.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        styles = response.choices[0].message.content
        cleaned_styles = extract_json(styles)

        try:
            parsed_styles = json.loads(cleaned_styles)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON received from OpenAI", "raw_output": styles}), 500

        default_styles = {
            "body": {},
            ".chat-box": {},
            ".button": {}
        }
        for key in default_styles:
            if key not in parsed_styles:
                parsed_styles[key] = default_styles[key]

        return jsonify({"styles": parsed_styles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
