from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import signal
import sys
from tools.post import postMsg
from tools import connect
from rich import print
from tools import error
from tools import cli
from tools import validate
import textwrap


def signal_handler(sig, frame):
    print('Received SIGINT, shutting down gracefully...')
    sys.exit(0)


# Define the HTTP request handler
class HTTPRequestHandler(BaseHTTPRequestHandler):

    def elasticsearch(self):
        try:
            es = connect.elasticsearch(args.es_host, args.es_port,
                                       args.es_user, args.es_pass,
                                       args.es_url_scheme,
                                       args.es_ssl_noverify)
            if es.ping():
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Elasticsearch OK")
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Elasticsearch Not OK")
        except:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Elasticsearch Not OK")

    def rabbitmq(self):
        print('checking rabbitmq')
        _, channel = connect.rabbitmq(args.rabbit_user,
                                      args.rabbit_pass,
                                      args.rabbit_host,
                                      args.rabbit_port,
                                      args.rabbit_vhost)
        if channel:
            channel.queue_declare(queue='healthcheck', durable=True)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"RabbitMQ OK")
        else:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"RabbitMQ Not OK")

    def default(self):
        if self.elasticsearch and self.rabbitmq:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"All systems OK")
        else:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Service Unavailable")

    def do_GET(self):
        if not self.path.startswith('/') or self.path == '/favicon.ico' and '?' not in self.path:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No no no... You didn\'t said the magic word')
            return

        elif self.path.startswith('/healthcheck'):
            # Parse query parameters
            query = urllib.parse.urlparse(self.path).query

            switch = {
                'elasticsearch': self.elasticsearch,
                'rabbitmq': self.rabbitmq,
                '': self.default,
            }
            switch[query]()

        elif self.path.startswith('/') and '?' in self.path:
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
            index_name = query_params.get('index_name', [''])[0]

            payload = {
                "project_id": project_id,
                "job_id": job_id,
                "runner_id": runner_id,
                "project_name": project_name,
                "job_name": job_name,
                "gitlab_token": gitlab_token,
                "index_name": index_name
            }

            if validate.mandatoryFields(payload):
                try:
                    connection, channel = connect.rabbitmq(args.rabbit_user,
                                                           args.rabbit_pass,
                                                           args.rabbit_host,
                                                           args.rabbit_port,
                                                           args.rabbit_vhost)
                except Exception:
                    error("Error connecting to RabbitMQ")

                if self.elasticsearch and self.rabbitmq:
                    postMsg(channel,
                            project_id,
                            job_id,
                            runner_id,
                            project_name,
                            job_name,
                            gitlab_token,
                            index_name,
                            args)

                # Send an HTTP response with the sum of the four variables
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK!')

            else:
                response = textwrap.dedent(f'''
                    Query params missing or invalid\n\n\
                    project_id=\'{project_id}\'\n\
                    job_id=\'{job_id}\'\n\
                    index_name=\'{index_name}\'\n\
                    gitlab_token=\'{gitlab_token}\'
                ''').strip()
                response = textwrap.dedent(response).strip()
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(response.encode("utf-8"))
        elif self.path == '/favicon.ico':
            return

        else:
            # Invalid endpoint
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"No no no... You didn\'t said the magic word")


global args

signal.signal(signal.SIGINT, signal_handler)

# Initialize CLI flags
args = cli.args()

# Start the web server on port 8080
httpd = HTTPServer(("", args.port), HTTPRequestHandler)
print("serving at port", args.port)
httpd.serve_forever()
