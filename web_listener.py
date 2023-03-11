from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import signal
import sys
from tools.post import postMsg
from tools import connect
from rich import print
from tools.error import error
from tools import cli


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    sys.exit(0)


# Define the HTTP request handler
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/favicon.ico':
            return

        try:
            # Parse the query parameters from the URL
            query_params = urllib.parse.parse_qs(
                urllib.parse.urlparse(self.path).query)

            # Extract the four integer variables from the query parameters
            project_id = query_params.get('project_id', [''])[0]
            job_id = query_params.get('job_id', [''])[0]
            runner_id = query_params.get('runner_id', [''])[0]
            project_name = query_params.get('project_name', [''])[0]
            job_name = query_params.get('job_name', [''])[0]
            gitlab_token = query_params.get('gitlab_token', [''])[0]

            try:
                connection, channel = connect.rabbitmq(args.rabbit_user,
                                                       args.rabbit_pass,
                                                       args.rabbit_host,
                                                       args.rabbit_port,
                                                       args.rabbit_vhost)
            except Exception:
                error("Error connecting to RabbitMQ")

            postMsg(channel,
                    project_id,
                    job_id,
                    runner_id,
                    project_name,
                    job_name,
                    gitlab_token,
                    args)

            # Send an HTTP response with the sum of the four variables
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK!')

        except (KeyError, ValueError) as e:
            # Handle exceptions for missing or invalid query parameters
            self.send_error(400, str(e))

        except Exception as e:
            # Handle other exceptions
            self.send_error(500, str(e))


global args

signal.signal(signal.SIGINT, signal_handler)

# Initialize CLI flags
args = cli.web()

# Start the web server on port 8080
httpd = HTTPServer(('localhost', args.port), MyHTTPRequestHandler)
print('Listening on port 8080...')
httpd.serve_forever()
