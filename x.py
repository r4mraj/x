from flask import Flask, request, render_template, jsonify
import json
import requests

app = Flask(__name__)

def get_facebook_data(cookie_string):
    try:
        # Parse the JSON cookie string into a dictionary
        cookies = json.loads(cookie_string)

        # Facebook URL to send the request
        url = "https://www.facebook.com"

        # Set up the headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": "https://www.facebook.com/",
            "DNT": "1"
        }

        # Make a GET request
        response = requests.get(url, headers=headers, cookies=cookies)

        # Check the response status
        if response.status_code == 200:
            # Extract the desired headers
            data = {
                "Content-Type": response.headers.get("Content-Type"),
                "Access-Control-Expose-Headers": response.headers.get("Access-Control-Expose-Headers"),
                "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials"),
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "fb-s": response.headers.get("fb-s"),
                "fb-ar": response.headers.get("fb-ar"),
                "reporting-endpoints": response.headers.get("reporting-endpoints"),
                "document-policy": response.headers.get("document-policy"),
                "permissions-policy": response.headers.get("permissions-policy"),
                "cross-origin-resource-policy": response.headers.get("cross-origin-resource-policy"),
                "Pragma": response.headers.get("Pragma"),
                "Cache-Control": response.headers.get("Cache-Control"),
                "Expires": response.headers.get("Expires"),
                "X-Content-Type-Options": response.headers.get("X-Content-Type-Options"),
                "report-to": response.headers.get("report-to"),
                "origin-agent-cluster": response.headers.get("origin-agent-cluster"),
                "Strict-Transport-Security": response.headers.get("Strict-Transport-Security"),
                "X-FB-Debug": response.headers.get("X-FB-Debug"),
                "Date": response.headers.get("Date"),
                "X-FB-Connection-Quality": response.headers.get("X-FB-Connection-Quality"),
                "Alt-Svc": response.headers.get("Alt-Svc"),
                "Connection": response.headers.get("Connection"),
                "Content-Length": response.headers.get("Content-Length"),
            }
            return data  # Return the extracted data
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except json.JSONDecodeError:
        return {"error": "Invalid cookie string format."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    cookie_string = request.form.get('cookie_string')
    result = get_facebook_data(cookie_string)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
      
