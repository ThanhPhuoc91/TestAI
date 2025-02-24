from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.gptgod.online/v1/chat/completions"
API_KEY = "sk-OsMMq65tXdfOIlTUYtocSL7NCsmA7CerN77OkEv29dODg1EA" # **Quan trọng: Nên dùng biến môi trường thay vì hardcode**

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text_to_translate = data.get('text')
        if not text_to_translate:
            return jsonify({"error": "Vui lòng cung cấp văn bản cần dịch trong trường 'text'."}), 400

        payload = {
            "model": "gpt-3.5-turbo", # Hoặc model khác bạn muốn dùng
            "messages": [
                {"role": "user", "content": f"Dịch đoạn văn bản sau từ tiếng Trung sang tiếng Việt: {text_to_translate}"}
            ]
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_BASE_URL, headers=headers, json=payload)
        response.raise_for_status() # Báo lỗi nếu request không thành công

        translation_result = response.json()
        translated_text = translation_result['choices'][0]['message']['content']

        return jsonify({"translated_text": translated_text})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Lỗi khi kết nối đến API gptgod.online: {e}"}), 500
    except KeyError as e:
        return jsonify({"error": f"Lỗi xử lý phản hồi API: Thiếu khóa '{e}'"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi không xác định: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Chạy server Flask