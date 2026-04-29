import json, re

def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {
        "enough": False,
        "question_for_user": "Bạn có thể cung cấp thêm thông tin chi tiết hơn không?"
    }