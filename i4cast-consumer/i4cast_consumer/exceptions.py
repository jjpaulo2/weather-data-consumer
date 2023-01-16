from typing import Self


class NotFoundEnvironmentalDataException(Exception):

    def __init__(self, station_id: int, env_type: str) -> Self:
        self.message = 'Não foi encontrado nenhum dado para os parâmetros fornecidos.'
        self.station_id = station_id
        self.env_type = env_type


class UnauthorizedException(Exception):

    def __init__(self) -> Self:
        self.message = 'Não foi possivel consumir a API com as credenciais fornecidas.'
