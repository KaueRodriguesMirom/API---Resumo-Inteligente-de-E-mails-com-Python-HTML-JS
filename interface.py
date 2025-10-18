import customtkinter as ctk
from gmail_reader import autenticar_gmail, ler_emails
from resumidor import resumir_texto

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Leitor de E-mails Inteligente")
app.geometry("800x600")

lista_emails = ctk.CTkTextbox(app, width=780, height=300)
lista_emails.pack(pady=10)

resumo_box = ctk.CTkTextbox(app, width=780, height=200)
resumo_box.pack(pady=10)

def iniciar_leitura():
    try:
        service = autenticar_gmail()
        emails = ler_emails(service)

        lista_emails.delete("0.0", "end")
        resumo_box.delete("0.0", "end")

        for email in emails:
            lista_emails.insert("end", f"ID: {email['id']}\nDe: {email['from']}\nData: {email['date']}\n{'-'*40}\n")
            resumo = resumir_texto(email['snippet'])
            resumo_box.insert("end", f"Resumo: {resumo}\n{'='*40}\n")
    except Exception as e:
        resumo_box.insert("end", f"Erro: {str(e)}\n")

botao = ctk.CTkButton(app, text="Autenticar e Ler E-mails", command=iniciar_leitura)
botao.pack(pady=10)

app.mainloop()
