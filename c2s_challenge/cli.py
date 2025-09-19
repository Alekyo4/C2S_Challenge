from typer import Typer

from c2s_challenge.server import make_server, ServerProvider

cli: Typer = Typer()

@cli.command()
def server() -> None:
  sv: ServerProvider = make_server()

  sv.listen()

@cli.command()
def client() -> None:
  print("Starting client...")

if __name__ == "__main__":
  cli()