import tkinter as tk
from tkinter import messagebox
import json 

class DataStorage:
    def __init__(self, file_name="car_database.json"):
        self.__file_name = file_name  
        self.__data = self.__load_data()  

    def __save_data(self):
        with open(self.__file_name, "w", encoding="utf-8") as file:
            json.dump(self.__data, file, indent=4)

    def __load_data(self):
        try:
            with open(self.__file_name, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def get_data(self):
        return self.__data

    def save(self):
        self.__save_data()


class CarDatabase(DataStorage):
    def __init__(self, file_name="car_database.json"):
        super().__init__(file_name)  # Chama o construtor da classe base

    def add_car(self, model, price):
        if model in self.get_data():
            return f"O modelo {model} já está cadastrado."
        else:
            self.get_data()[model] = price
            self.save()  # Salva após a modificação
            return f"Modelo {model} adicionado com sucesso!"

    def update_price(self, model, new_price):
        if model in self.get_data():
            self.get_data()[model] = new_price
            self.save()  # Salva após a modificação
            return f"Preço do modelo {model} atualizado para R$ {new_price}."
        else:
            return f"O modelo {model} não foi encontrado."

    def delete_car(self, model):
        if model in self.get_data():
            del self.get_data()[model]
            self.save()  # Salva após a modificação
            return f"Modelo {model} removido com sucesso!"
        else:
            return f"O modelo {model} não foi encontrado."

    def list_cars(self):
        if not self.get_data():
            return "Nenhum carro cadastrado."
        else:
            return "\n".join([f"- {model}: R$ {price}" for model, price in self.get_data().items()])


# Interface Gráfica com tkinter
class CarDatabaseGUI:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.root.title("Menu para cadastramento de carros")
        self.root.geometry("400x400")

        # Label de título
        self.title_label = tk.Label(root, text="Sistema de Cadastro de Carros", font=("Arial", 14))
        self.title_label.pack(pady=10)

        # Campo para o modelo do carro
        self.model_label = tk.Label(root, text="Modelo do Carro")
        self.model_label.pack()
        self.model_entry = tk.Entry(root)
        self.model_entry.pack(pady=5)

        # Campo para o preço do carro
        self.price_label = tk.Label(root, text="Preço do Carro")
        self.price_label.pack()
        self.price_entry = tk.Entry(root)
        self.price_entry.pack(pady=5)

        # Botões
        self.add_button = tk.Button(root, text="Adicionar Carro", command=self.add_car)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Atualizar Preço", command=self.update_price)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Remover Carro", command=self.delete_car)
        self.delete_button.pack(pady=5)

        self.list_button = tk.Button(root, text="Listar Carros", command=self.list_cars)
        self.list_button.pack(pady=5)

        # Caixa de texto para exibir a lista de carros
        self.text_box = tk.Text(root, width=40, height=10)
        self.text_box.pack(pady=10)

    def add_car(self):
        """Adicionar um carro ao banco de dados."""
        model = self.model_entry.get()
        price = self.price_entry.get()

        if not model or not price:
            messagebox.showerror("Erro", "Por favor, preencha o modelo e o preço.")
            return

        try:
            price = float(price)
            result = self.database.add_car(model, price)
            messagebox.showinfo("Resultado", result)
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido. Digite um número.")

    def update_price(self):
        """Atualizar o preço de um carro."""
        model = self.model_entry.get()
        price = self.price_entry.get()

        if not model or not price:
            messagebox.showerror("Erro", "Por favor, preencha o modelo e o novo preço.")
            return

        try:
            price = float(price)
            result = self.database.update_price(model, price)
            messagebox.showinfo("Resultado", result)
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido. Digite um número.")

    def delete_car(self):
        """Remover um carro do banco de dados."""
        model = self.model_entry.get()

        if not model:
            messagebox.showerror("Erro", "Por favor, preencha o modelo.")
            return

        result = self.database.delete_car(model)
        messagebox.showinfo("Resultado", result)
        self.clear_entries()

    def list_cars(self):
        """Exibir todos os carros cadastrados."""
        cars = self.database.list_cars()
        self.text_box.delete(1.0, tk.END)  # Limpar a caixa de texto
        self.text_box.insert(tk.END, cars)

    def clear_entries(self):
        """Limpar os campos de entrada."""
        self.model_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


# Exemplo de uso do Tkinter
if __name__ == "__main__":
    database = CarDatabase()  # Cria a instância do banco de dados
    root = tk.Tk()  # Cria a janela principal
    gui = CarDatabaseGUI(root, database)  # Passa a instância da GUI para a janela
    root.mainloop()  # Inicia o loop principal do Tkinter
