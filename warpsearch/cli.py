import click
import os
import subprocess
import shlex
from warpsearch.vectorstore import *

import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

@click.group()
@click.version_option()
def cli():
    "A local image search engine"

@cli.command(name="setup")
@click.argument("folder_path")
def monitor(folder_path):
    """Monitors a folder for changes and runs a script on each change."""
    script_path = 'warpsearch/monitor_script.sh'
    click.echo(f"Monitoring changes in: {folder_path}")
    
    # Command to keep the process running in the background even if the terminal is closed
    bg_cmd = f"nohup {shlex.quote(script_path)} {shlex.quote(folder_path)} > fswatch.log 2>&1 &"

    # Execute the command
    subprocess.run(bg_cmd, shell=True, check=True)
    click.echo("Monitoring started in the background.")


@cli.command(name="find")
@click.argument(
    "query_text"
)
def query(query_text):
    "Finds and opens images matching given query"
    vector_store = VectorStore()
    #entries overlap each other when opened, show most relevant last
    results = vector_store.query(query_text)['metadatas'][0][::-1]
    click.echo(f"Found a match: {click.format_filename(f'{results}')}")
    for entry in results:
        click.launch(entry['filename']) #add locate=True to point instead of open

@cli.command(name="info")
def vault_info():
    "Returns vault location and its file count"
    vector_store = VectorStore()
    vector_store_count = vector_store.get_collection().count()
    with open('./fswatch.log', 'r') as log_file:
        first_line = log_file.readline()
        vault_location = first_line.split('] ')[1].strip()
    click.echo("+----------------+--------------------------------+")
    click.echo("| Vault Location | {:<30} |".format(vault_location))
    click.echo("+----------------+--------------------------------+")
    click.echo("| Total Files    | {:<30} |".format(vector_store_count))
    click.echo("+----------------+--------------------------------+")


@cli.command(name="purge")
def purge_entries():
    "Purges all entries from the vector store."
    vector_store = VectorStore()
    vector_store.purge()
    click.echo("All entries have been purged from the vector store.")
