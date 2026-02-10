from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

subscriptions = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Subscription Tracker</title>
    <style>view
    
        body {
            font-family: Segoe UI, Tahoma, sans-serif;
            background: linear-gradient(120deg, #89f7fe, #66a6ff);
            margin: 0;
            padding: 0;
        }
        .card {
            width: 420px;
            margin: 60px auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }
        h1, h2, h3 {
            text-align: center;
            color: #333;
        }
        p {
            text-align: center;
            color: #666;
        }
        label {
            font-weight: bold;
            color: #555;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            margin-bottom: 14px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(45deg, #43e97b, #38f9d7);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
        }
        button:hover {
            opacity: 0.9;
        }
        .sub {
            background: #f0f4ff;
            padding: 12px;
            margin-top: 10px;
            border-left: 5px solid #66a6ff;
            border-radius: 6px;
        }
        a {
            display: inline-block;
            margin-top: 15px;
            color: #0077cc;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<div class="card">
__CONTENT__
</div>
</body>
</html>
"""

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            content = """
            <h1>Subscription Manager</h1>
            <p>Track and manage your subscriptions easily</p>

            <form method="post">
                <label>Service Name</label>
                <input name="name" required>

                <label>Monthly Cost (INR)</label>
                <input name="amount" required>

                <label>Next Renewal Date</label>
                <input name="date" placeholder="YYYY-MM-DD" required>

                <button>Add Subscription</button>
            </form>

            <a href="/view">View All Subscriptions</a>
            """
            self.respond(content)

        elif self.path == "/view":
            content = "<h2>Your Active Subscriptions</h2>"
            for s in subscriptions:
                content += f"""
                <div class="sub">
                    <b>Service:</b> {s[0]}<br>
                    <b>Amount:</b> INR {s[1]}<br>
                    <b>Renewal Date:</b> {s[2]}
                </div>
                """
            content += "<a href='/'>Go Back</a>"
            self.respond(content)

    def do_POST(self):
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length).decode()
        form = parse_qs(data)

        name = form["name"][0]
        amount = form["amount"][0]
        date = form["date"][0]

        subscriptions.append((name, amount, date))

        content = """
        <h3>Subscription Added Successfully</h3>
        <p>Your subscription details have been saved.</p>
        <a href="/">Add Another Subscription</a><br>
        <a href="/view">View Subscriptions</a>
        """
        self.respond(content)

    def respond(self, content):
        page = HTML_TEMPLATE.replace("__CONTENT__", content)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode())

# Start server
server = HTTPServer(("localhost", 8000), MyHandler)
print("Website running at http://localhost:8000")
server.serve_forever()
