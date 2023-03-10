from rich import print
import json


def postMsg(channel, project_id, job_id, runner_id, project_name,
            job_name, gitlab_token, args):
    message_body = {
        'url': args.gitlab_url + str(project_id) + '/jobs/' + str(job_id) + '/trace',
        'runner_id': runner_id,
        'project_id': project_id,
        'job_id': job_id,
        'job_name': job_name,
        'project_name': project_name,
        'gitlab_token': gitlab_token
    }
    message_json = json.dumps(message_body)
    if args.debug:
        print(f'[green]Pushing message:[/green] {message_body}')
    channel.basic_publish(exchange=args.rabbit_exchange,
                          routing_key=args.rabbit_route_key,
                          body=message_json)
