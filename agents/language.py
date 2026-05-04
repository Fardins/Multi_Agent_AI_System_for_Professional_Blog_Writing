import re


def detect_language(state: dict) -> dict:
    topic = state.get("topic", "")
    # Bangla Unicode block: U+0980–U+09FF
    if re.search(r"[\u0980-\u09FF]", topic):
        language = "bn"
    else:
        language = "en"
    return {"language": language}