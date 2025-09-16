from typer import Typer

cli: Typer = Typer()

@cli.command()
def main() -> None:
  print("WORKING")

if __name__ == "__main__":
  cli()