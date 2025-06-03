from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    token = ""
    error = None

    if request.method == 'POST':
        token = request.form['token']
        url = f'https://graph.facebook.com/v20.0/me/groups?fields=name,id&limit=1000&access_token={token}'

        try:
            response = requests.get(url)
            data = response.json()

            if 'data' in data:
                for group in data['data']:
                    groups.append({
                        'name': group.get('name', 'No Name'),
                        'uid': group.get('id')
                    })
            else:
                error = data.get("error", {}).get("message", "Something went wrong.")
        except Exception as e:
            error = str(e)

    return render_template('index.html', groups=groups, token=token, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
