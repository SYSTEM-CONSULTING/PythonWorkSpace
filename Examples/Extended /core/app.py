from services.user_service import UserService
from services.printer_service import PrinterService
from services.calculation_service import CalculationService

class App:
    def __init__(self):
        self.user_service=UserService()
        self.printer_service=PrinterService()
        self.calc=CalculationService()
    def run(self):
        print('=== Example App gestartet ===')
        print('Benutzer:', self.user_service.list_users())
        print('Berechnung 5+7=', self.calc.add(5,7))
        print('Drucker:', self.printer_service.list_printers())
