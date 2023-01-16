from asyncio.exceptions import CancelledError
from argparse import ArgumentParser
from sys import exit

from i4cast_consumer.exceptions import NotFoundEnvironmentalDataException
from i4cast_consumer.app import run_main
from i4cast_consumer.models import EnvironmentalType
from i4cast_consumer import (
    __author__,
    __title__,
    __version__
)


def get_args_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='i4cast_consumer',
        description=f'{__title__} v{__version__}, by {__author__}',
    )

    parser.add_argument('-s', '--station', default=None, required=False, type=int)
    parser.add_argument('-e', '--environment_type', default=None, required=False, type=EnvironmentalType)

    return parser


def cli() -> None:
    cli_args = get_args_parser().parse_args()
    module_args = {}

    if cli_args.station and cli_args.environment_type:
        module_args = {
            'station_id': cli_args.station,
            'env_type': cli_args.environment_type
        }

    try:
        run_main(**module_args)

    except NotFoundEnvironmentalDataException as exc:
        print(
            exc.message,
            f'station_id: \'{exc.station_id}\'.',
            f'env_type: \'{exc.env_type}\'.'
        )
        exit(-1)

    except CancelledError:
        print('\nEncerrando o programa...')
        exit(-1)


if __name__ == '__main__':
    cli()
