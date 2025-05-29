import requests
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

API_KEY = "Enter your valid Groq Cloud API key here (it's free)" 
conversation_history = []
is_dark = False

def toggle_theme():
    global is_dark

    bg_color = "#222222" if not is_dark else "lightgray"
    fg_color = "white" if not is_dark else "black"

    root.configure(bg=bg_color)

    widgets = [
        chat_area,
        label1,
        user_input,
        send_btn,
        clear_chat_btn,
        toggle_theme_btn,
        exit_btn
    ]

    for widget in widgets:
        widget.configure(bg=bg_color, fg=fg_color)

    
    chat_area.configure(insertbackground=fg_color)
    user_input.configure(insertbackground=fg_color)

    is_dark = not is_dark


def chat_with_ai(prompt):
    try:
        
        conversation_history.append({"role": "user", "content": prompt})
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-type": "application/json"
        }
                
        data = {
            "messages": conversation_history,
            "model": "llama3-8b-8192"
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        reply = response.json()['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": reply}) 
        return reply

    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to get response from AI:\n{e}")
        return "[Error] Could not connect to the API."

    except KeyError:
        messagebox.showerror("API Error", "Unexpected response structure from API.")
        return "[Error] Invalid response from API."

    except Exception as e:
        return f"[Error] {str(e)}"
def chatbot(event=None):

    user_text = user_input.get().strip()
    user_input.delete(0, tk.END)

    if user_text == "":
        return
    
    chat_area.insert(tk.END, f"You: {user_text}\n")

    if user_text.lower() in ["exit", "quit", "bye"]:
        chat_area.insert(tk.END, "Bot: GoodBye!!\n")
        root.after(1500, root.quit)
        return

    chat_area.insert(tk.END, "Bot: Typing...\n")
    chat_area.see(tk.END)

    def show_response():
        
        chat_area.delete("end-2l", "end-1l")        
        response = chat_with_ai(user_text)
        chat_area.insert(tk.END, f"Bot: {response}\n\n")
        chat_area.see(tk.END)


    root.after(1500, show_response)

def clear_chat():
    chat_area.delete(1.0, tk.END)
    conversation_history.clear()
root = tk.Tk()
root.title("--- Mini AI Agent ---")
root.geometry('900x900')
root.resizable(True, True)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


label1 = tk.Label(root, text="Enter your chat here: ", font=("Arial", 12), width=20, height=2)
label1.pack(pady=5)

user_input = tk.Entry(root, justify='center', font=("Arial", 12), width=80)
user_input.pack(pady=5)
user_input.focus()


send_btn = tk.Button(root, text="Send", command=chatbot, font=("Arial", 12), width=20, height=2)
send_btn.pack(pady=5)

clear_chat_btn = tk.Button(root, text="Clear Chat", command=clear_chat, font=("Arial", 12), width=20, height=2)
clear_chat_btn.pack(pady=5)

toggle_theme_btn = tk.Button(root, text="Toggle Theme", command=toggle_theme, font=("Arial", 12), width=20, height=2)
toggle_theme_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), width=20, height=2)
exit_btn.pack(pady=5)

root.bind("<Return>", chatbot)
if __name__ == '__main__':
    root.mainloop()