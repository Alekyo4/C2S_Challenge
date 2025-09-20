from asyncio import run as asyncio

from typer import Typer

from c2s_challenge.server import make_server_async

cli: Typer = Typer()

@cli.command()
def server() -> None:
  async def run_server_async() -> None:
    async with make_server_async() as sv:
      await sv.listen()

  asyncio(run_server_async())

@cli.command()
def client() -> None:
  print("Starting client...")

if __name__ == "__main__":
  cli()