import json
import streamlit.components.v1 as components


def speak_button(text):

    if not text:
        return

    safe_text = json.dumps(text)

    components.html(
    f"""
    <html>
    <body style="margin:0;padding:0;overflow:hidden;background:transparent;">

    <script>
        window.speechSynthesis.cancel();

        const msg = new SpeechSynthesisUtterance({safe_text});

        if(/[\\u0900-\\u097F]/.test({safe_text})) {{
            msg.lang = "hi-IN";
        }} else {{
            msg.lang = "en-US";
        }}

        msg.rate = 1;
        msg.pitch = 1;
        msg.volume = 1;

        window.speechSynthesis.speak(msg);
    </script>

    </body>
    </html>
    """,
    height=1,
)