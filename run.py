import tkinter as tk
from PIL import Image, ImageTk
import threading
from cli_chat import chat_once, speak
import time


LOADING_SECONDS = 3

class LoadingScreen(tk.Frame):
    def __init__(self, parent, on_finish):
        super().__init__(parent, bg="#1e1e1e")
        self.on_finish = on_finish
        self.remaining = LOADING_SECONDS

        self.pack(expand=True, fill="both")

        self.label = tk.Label(
            self,
            text="Axienta AI",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 26, "bold")
        )
        self.label.pack(pady=40)

        self.timer_lbl = tk.Label(
            self,
            text="Starting...",
            fg="white",
            bg="#1e1e1e",
            font=("Arial", 14)
        )
        self.timer_lbl.pack()

        self._tick()

    def _tick(self):
        if self.remaining > 0:
            self.timer_lbl.config(text=f"Starting in {self.remaining}...")
            self.remaining -= 1
            self.after(1000, self._tick)
        else:
            self.destroy()
            self.on_finish()

class ChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Axienta AI chatbot")
        self.root.geometry("400x600+500+100")

        self.text_area = tk.Text(root, state="disabled", wrap="word", font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, expand=True, fill="both")
        self.text_area.tag_configure(
            "user",
            background="#DCF8C6",   # light green (WhatsApp style)
            foreground="black",
            spacing1=5,
            spacing3=5
        )

        self.text_area.tag_configure(
            "bot",
            background="#F1F0F0",   # light gray
            foreground="black",
            spacing1=5,
            spacing3=5
        )


        self.bottom_lbl = tk.Label(background="purple")
        self.bottom_lbl.place(relx=0.0, rely=0.9, relwidth=1.0, relheight=0.1)

        self.entry = tk.Entry(self.bottom_lbl, font=("Arial", 15))
        self.entry.place(relx=0.01, rely=0.2, relwidth=0.80, relheight=0.6)
        self.placeholder = "Type your message..."
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg="gray")
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._add_placeholder)

        

        # Load icon image
        icon_img = Image.open("res//send.png")
        icon_img = icon_img.resize((24, 24), Image.LANCZOS)

        self.send_icon = ImageTk.PhotoImage(icon_img)

        self.send_btn = tk.Label(
        self.bottom_lbl,
        image=self.send_icon,
        bg="purple",
        cursor="hand2")

        self.send_btn.place(relx=0.87, rely=0.15, relwidth=0.06, relheight=0.7)

        # Click event
        self.send_btn.bind("<Button-1>", self.send_message)

    def _append_text(self, text, tag=None):
        self.text_area.config(state="normal")

        if tag:
            # Insert text WITH background
            self.text_area.insert(tk.END, text, tag)
            # Insert newline WITHOUT background
            self.text_area.insert(tk.END, "\n")
        else:
            self.text_area.insert(tk.END, text + "\n")

        self.text_area.config(state="disabled")
        self.text_area.see(tk.END)

    def _clear_placeholder(self, event=None):
            if self.entry.get() == self.placeholder:
                self.entry.delete(0, tk.END)
                self.entry.config(fg="black")

    def _add_placeholder(self, event=None):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray")
    
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, tk.END)

        if not user_input or user_input == self.placeholder:
            return

        self.entry.delete(0, tk.END)
        self._add_placeholder()
        

        self._append_text(f"You: {user_input}\n", "user")

        reply = chat_once(user_input)
        self._append_text(f"Bot: {reply}\n","bot")
        speak(reply)

        #threading.Thread(target=self._get_response,args=(user_input,),daemon=True).start()
        
def start_chat():
    ChatUI(root)

root = tk.Tk()
root.title("Axienta Chatbot")
root.geometry("400x600+500+100")
root.resizable(False, False)

LoadingScreen(root, start_chat)

root.mainloop()