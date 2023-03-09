from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import signal
import sys
from tools.post import postMsg
from tools.connect import connect
import argparse


# Variables
exchange_name = 'gitlab_exchange'
routing_key = 'jobs'

base_path = 'https://gitlab.com/api/v4/projects/'


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    # Add cleanup code here
    sys.exit(0)


# Define the HTTP request handler
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/favicon.ico':
            # Return a 404 error response for the favicon request
            # self.send_error(404, 'File not found')
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

            postMsg(channel,
                    base_path,
                    project_id,
                    job_id,
                    runner_id,
                    project_name,
                    job_name,
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


signal.signal(signal.SIGINT, signal_handler)


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Start a web server to handle \
                                 GET requests from Gitlab pipelines which \
                                 are being posted to RabbitMQ for further \
                                 processing.')
parser.add_argument('-p', dest='port', type=int, default=8080,
                    help='The port to listen on [Default: 8080]')
parser.add_argument('--user', dest='rabbit_user', type=str,
                    required=True, help='RabbitMQ Username')
parser.add_argument('--pass', dest='rabbit_pass', type=str,
                    required=True, help='RabbitMQ Password')
parser.add_argument('--host', dest='rabbit_host', type=str,
                    required=True, help='RabbitMQ Host')
parser.add_argument('--port', dest='rabbit_port', type=int,
                    default=5672, help='RabbitMQ Port [Default: 5672]')
parser.add_argument('--vhost', dest='rabbit_vhost', type=str,
                    default='my_vhost', help='RabbitMQ VHost \
                        [Default: my_vhost]')
parser.add_argument('--exchange', dest='rabbit_exchange', type=str,
                    default='gitlab_exchange', help='RabbitMQ Exchange \
                        [Default: gitlab_exchange]')
parser.add_argument('--routekey', dest='rabbit_route_key', type=str,
                    default='jobs', help='RabbitMQ Exchange Routing Key \
                        [Default: jobs]')
parser.add_argument('--debug', action='store_true', help='enable debug mode')

args = parser.parse_args()


# Start the web server on port 8080
connection, channel = connect(args.rabbit_user, args.rabbit_pass,
                              args.rabbit_host, args.rabbit_port,
                              args.rabbit_vhost)

httpd = HTTPServer(('localhost', args.port), MyHTTPRequestHandler)
print('Listening on port 8080...')
httpd.serve_forever()
