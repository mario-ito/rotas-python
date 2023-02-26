import json
import requests
import urllib.parse

from Helpers.input import *
from Classes.Presenter import Presenter
from requests.structures import CaseInsensitiveDict
from os import getenv
from dotenv import load_dotenv

class Routes:

    def __init__(self, presenter: Presenter):
        load_dotenv()
        self.address_from = {}
        self.address_to = {}
        self.apiKey = getenv('API_KEY')
        self.presenter = presenter

    @staticmethod
    def __request_api(url):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        resp = requests.get(url=url, headers=headers)
        return json.loads(resp.content) if resp.status_code == 200 else None

    def __request_geocode(self, params):
        """ Requisição de Geocode com a API GeoApify """
        url = "https://api.geoapify.com/v1/geocode/search?" + urllib.parse.urlencode(params)
        return self.__request_api(url)

    def __request_route(self):
        """ Requisição de Rota com a API GeoApify """
        coords_url = self.__coords_url(self.address_from) + "|" + self.__coords_url(self.address_to)
        url = f"https://api.geoapify.com/v1/routing?waypoints={coords_url}&mode=drive&lang=pt-BR&apiKey={self.apiKey}"
        return self.__request_api(url)

    @staticmethod
    def __coords_url(address):
        """ Formata coordenadas para enviar para a api via GET """
        coords = address["geometry"]["coordinates"]
        return str(coords[1]) + ',' + str(coords[0])


    def __input_dict(self, address_type):
        """ #address_type = origem ou destino """
        adr_t = address_type.title()
        return {
            "street": input_required(f"Informe o logradouro de {adr_t} (exemplo: rua da Consolação): "),
            "housenumber": input_required(f"Informe o número de {adr_t} (apenas dígitos): "),
            "city": input_required(f"Informe a cidade de {adr_t}: "),
            "state": input_required(f"Informe o estado de {adr_t} (no formato UF, exemplo: SP): "),
            "apiKey": self.apiKey
        }


    def __get_address(self, address_type):
        """ #address_type = origem ou destino """
        print(f"Endereço de {address_type.title()}")
        params = self.__input_dict(address_type)
        api_response = self.__request_geocode(params)
        return self.__select_address(api_response["features"], address_type) if api_response else None


    def __select_address(self, address_list, address_type):
        """ Seleciona o endereço correto """
        for i, address in enumerate(address_list):
            print("ID " + str(i + 1) + " : " + address["properties"]["formatted"])

        msg = f"\nConfirme o endereço de {address_type} digitando seu ID ou digite E para informar os dados do endereço novamente: "

        address_index = input_in_range(msg, range(1, len(address_list) + 1), 'E')
        if str(address_index).upper() == 'E':
            self.__get_address(address_type)
        else:
            self.presenter.print_success(f"Endereço de {address_type} definido com sucesso\n")
            return address_list[address_index - 1]


    def get_route(self):
        self.presenter.print_title("Consultar rota")

        self.address_from = self.__get_address("origem")
        if not self.address_from:
            self.presenter.print_error("Não foi possível consultar o endereço")
            wait_input()
            return True

        self.address_to = self.__get_address("destino")
        if not self.address_to:
            self.presenter.print_error("Não foi possível consultar o endereço")
            wait_input()
            return True

        route = self.__request_route()
        self.print_route(route)


    def print_route(self, route):
        self.presenter.print_title(f"ROTA DE:\n" + self.address_from["properties"]["formatted"] + "\nPARA:\n" + self.address_to["properties"][
            "formatted"])

        try:
            distance = route["features"][0]["properties"]["distance"]
            time = route["features"][0]["properties"]["time"]
            distance = round(distance / 1000, 1)
            time = round(time / 60)
            print(f"\nDistância: {distance}km")
            print(f"Tempo Estimado: {time} minutos\n")

            user_input = input("Deseja ver a rota detalhada?: ")
            if user_input.lower() == 'sim' or user_input.lower() == 's':
                steps = route["features"][0]["properties"]["legs"][0]["steps"]
                for step in steps:
                    print(f"Após {step['distance']} metros: {step['instruction']['text']}")
                wait_input()
        except:
            self.presenter.print_error("Erro a o calcular a rota")
            wait_input()
            pass
