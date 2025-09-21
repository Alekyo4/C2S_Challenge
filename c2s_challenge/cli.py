from asyncio import run as asyncio

from typer import Typer

# > Client
from c2s_challenge.client import make_client_async, make_vehicle_agent
from c2s_challenge.client.agent import VehicleAgent

# > Server
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
    async def run_client_async() -> None:
        async with make_client_async() as cl:
            agent: VehicleAgent = await make_vehicle_agent(client=cl)

            await agent.run_interactive()

    asyncio(run_client_async())


if __name__ == "__main__":
    cli()
