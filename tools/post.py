from rich import print
import json


def postMsg(channel, base_path, project_id, job_id, runner_id, project_name,
            job_name, args):
    message_body = {
        'url': base_path + str(project_id) + '/jobs/' + str(job_id) + '/trace',
        'runner_id': runner_id,
        'project_id': project_id,
        'job_id': job_id,
        'job_name': job_name,
        'project_name': project_name
    }
    message_json = json.dumps(message_body)
    if args.debug:
        print(f'[green]Pushing message:[/green] {message_body}')
    channel.basic_publish(exchange=args.rabbit_exchange,
                          routing_key=args.rabbit_route_key,
                          body=message_json)