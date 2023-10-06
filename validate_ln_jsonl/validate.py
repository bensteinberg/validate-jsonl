import click
import json
from jsonschema import validate


@click.command()
@click.option('--schema', default='citations.json')
@click.option('--jsonl', default='lines.jsonl')
def cli(schema, jsonl):
    """ Validates a JSONL file according to a schema """

    with open(schema, 'r') as f:
        schema = json.load(f)

    exceptions = []

    with open(jsonl, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            line_number = idx + 1
            try:
                validate(instance=json.loads(line), schema=schema)
            except Exception as e:
                exceptions.append(str(line_number))
                print(f'Exception at line {line_number}: {e}')

        s = 's' if line_number > 1 else ''
        click.echo(f'Info: Read {line_number} line{s} in {jsonl}.')

        if exceptions:
            s = 's' if len(exceptions) > 1 else ''
            raise click.ClickException(
                f'Validation failed with {len(exceptions)} exception{s}, at line{s} {", ".join(exceptions)}.'  # noqa
            )
