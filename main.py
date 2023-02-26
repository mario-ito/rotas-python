from Classes.Presenter import Presenter
from Classes.Routes import Routes

presenter = Presenter()
route_class = Routes(presenter)

presenter.print_title("#### Consulta de rotas entre dois pontos ####")

route_class.get_route()

# Finalizando fluxo
presenter.print_title("Obrigado por usar a consulta de rotas")
