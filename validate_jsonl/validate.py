import click
import json
from collections import defaultdict
from jsonschema import validate


@click.command()
@click.option('--schema', default='citations.json')
@click.option('--jsonl', default='lines.jsonl')
def cli(schema, jsonl):
    """ Validates a JSONL file according to a schema """

    with open(schema, 'r') as f:
        schema = json.load(f)

    exceptions = defaultdict(list)

    with open(jsonl, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            line_number = idx + 1
            try:
                validate(instance=json.loads(line), schema=schema)
            except Exception as e:
                err = str(e).splitlines()[0]
                exceptions[err].append(str(line_number))
                click.echo(f'Exception at line {line_number}: {err}')

        s = 's' if line_number > 1 else ''
        click.echo(f'Info: Read {line_number} line{s} in {jsonl}.')

        if exceptions:
            s = 's' if len(exceptions) > 1 else ''
            msg = '\n\n'
            for err, lst in exceptions.items():
                msg += f'{err} at lines {", ".join(exceptions[err])}\n\n'
            raise click.ClickException(msg)
