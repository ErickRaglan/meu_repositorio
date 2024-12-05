from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp

# Dados atualizados com valores reais de benchmark
components_data = {
    "GPUs": {
        "GTX 1050": {"score": 3473},
        "GTX 1650": {"score": 5917},
        "GTX 1660 Super": {"score": 9029},
        "GTX 1080": {"score": 11052},
        "RTX 2060": {"score": 13286},
        "RTX 3060": {"score": 17367},
        "RTX 3070": {"score": 19059},
        "RTX 3080": {"score": 23302},
        "RTX 4090": {"score": 34114},
        "AMD RX 580": {"score": 6898},
        "AMD RX 6600": {"score": 10567},
        "AMD RX 6700 XT": {"score": 17470},
        "AMD RX 7900 XTX": {"score": 31067},
    },
    "CPUs": {
        "Intel i3-8100": {"score": 6000},
        "Intel i5-8400": {"score": 9200},
        "Intel i5-9600K": {"score": 12000},
        "Intel i7-9700K": {"score": 15500},
        "Intel i9-9900K": {"score": 22000},
        "Intel i5-12600K": {"score": 23000},
        "Intel i9-13900K": {"score": 40000},
        "AMD Ryzen 3 3200G": {"score": 6000},
        "AMD Ryzen 5 3600": {"score": 17000},
        "AMD Ryzen 5 5600X": {"score": 19000},
        "AMD Ryzen 7 5800X": {"score": 22000},
        "AMD Ryzen 9 5900X": {"score": 31000},
        "AMD Ryzen 7 7800X3D": {"score": 38000},
    },
}

# Interface KV
KV = '''
ScreenManager:
    WelcomeScreen:
    CalculatorScreen:

<WelcomeScreen>:
    name: 'welcome'

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            text: "Bem-vindo à Calculadora de Gargalo"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "Ir para a Calculadora"
            pos_hint: {"center_x": 0.5}
            on_release: app.change_screen('calculator')

<CalculatorScreen>:
    name: 'calculator'

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        MDLabel:
            text: "Selecione a CPU e a GPU para calcular o gargalo"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: cpu_dropdown
            hint_text: "Selecionar CPU"
            on_focus: if self.focus: app.open_cpu_menu()
            readonly: True

        MDTextField:
            id: gpu_dropdown
            hint_text: "Selecionar GPU"
            on_focus: if self.focus: app.open_gpu_menu()
            readonly: True

        MDRaisedButton:
            text: "Calcular Gargalo"
            pos_hint: {"center_x": 0.5}
            on_release: app.calculate_bottleneck()

        MDLabel:
            id: result_label
            text: "Resultado aparecerá aqui"
            halign: "center"
            font_style: "H6"
'''

class WelcomeScreen(Screen):
    pass

class CalculatorScreen(Screen):
    pass

class BottleneckApp(MDApp):
    def build(self):
        self.title = "Calculadora de Gargalo de CPU e GPU"
        self.data = components_data
        self.cpu_selected = None
        self.gpu_selected = None

        # Carregar a interface
        screen_manager = Builder.load_string(KV)

        # Criar menus para CPU e GPU
        self.cpu_menu = MDDropdownMenu(
            caller=screen_manager.get_screen('calculator').ids.cpu_dropdown,
            items=[ 
                {"text": key, "viewclass": "OneLineListItem", "on_release": lambda x=key: self.set_cpu(x)} 
                for key in self.data["CPUs"].keys()
            ],
            width_mult=4,
        )

        self.gpu_menu = MDDropdownMenu(
            caller=screen_manager.get_screen('calculator').ids.gpu_dropdown,
            items=[ 
                {"text": key, "viewclass": "OneLineListItem", "on_release": lambda x=key: self.set_gpu(x)} 
                for key in self.data["GPUs"].keys()
            ],
            width_mult=4,
        )

        return screen_manager

    def change_screen(self, screen_name):
        """Altera para a tela especificada."""
        self.root.current = screen_name

    def open_cpu_menu(self):
        """Abre o menu de seleção de CPU.""" 
        self.cpu_menu.open()

    def open_gpu_menu(self):
        """Abre o menu de seleção de GPU."""
        self.gpu_menu.open()

    def set_cpu(self, cpu_name):
        """Define a CPU selecionada e atualiza o texto do campo."""
        self.cpu_selected = cpu_name
        self.root.get_screen('calculator').ids.cpu_dropdown.text = cpu_name
        self.cpu_menu.dismiss()

    def set_gpu(self, gpu_name):
        """Define a GPU selecionada e atualiza o texto do campo."""
        self.gpu_selected = gpu_name
        self.root.get_screen('calculator').ids.gpu_dropdown.text = gpu_name
        self.gpu_menu.dismiss()

    def calculate_bottleneck(self):
        """Calcula e exibe o gargalo entre a CPU e GPU selecionadas."""
        if not self.cpu_selected or not self.gpu_selected:
            self.root.get_screen('calculator').ids.result_label.text = "Selecione uma CPU e uma GPU."
            return

        cpu_score = self.data["CPUs"][self.cpu_selected]["score"]
        gpu_score = self.data["GPUs"][self.gpu_selected]["score"]

        if cpu_score < gpu_score:
            bottleneck = ((gpu_score - cpu_score) / gpu_score) * 100
            result = f"Gargalo de {bottleneck:.2f}% (CPU limitando)"
        else:
            bottleneck = ((cpu_score - gpu_score) / cpu_score) * 100
            result = f"Gargalo de {bottleneck:.2f}% (GPU limitando)"

        # Adicionando lógica de recomendação
        if bottleneck > 30:
            result += "\nO gargalo está muito alto! Não é recomendado usar essas peças juntas."
        else:
            result += "\nEsta combinação é equilibrada. Ideal para um bom desempenho."

        self.root.get_screen('calculator').ids.result_label.text = result

if __name__ == "__main__":
    BottleneckApp().run()
