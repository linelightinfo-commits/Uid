from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    error = None
    if request.method == 'POST':
        token = request.form['token']
        url = f"https://graph.facebook.com/v19.0/me/groups?fields=id,name&limit=500&access_token={token}"
        try:
            r = requests.get(url)
            data = r.json()
            if 'data' in data:
                groups = data['data']
            else:
                error = data.get('error', {}).get('message', 'Unknown error')
        except Exception as e:
            error = str(e)
    return render_template('index.html', groups=groups, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
