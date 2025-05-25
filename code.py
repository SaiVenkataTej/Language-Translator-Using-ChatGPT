import os
import tkinter as tk
from tkinter import ttk, messagebox
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file variables

api_key = os.getenv("OPENAI_API_KEY")
def get_translation(text, source_lang, target_lang):

    if not api_key: raise ValueError("Set OPENAI_API_KEY")
    client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
    prompt = f"Translate from {source_lang} to {target_lang}: {text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful translator."},
                      {"role": "user", "content": prompt}],
            max_tokens=500)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def translate():
    try:
        txt = inputTextEntry.get("1.0", tk.END).strip()
        if not txt: outputText.config(state=tk.NORMAL); outputText.delete("1.0", tk.END); outputText.insert(tk.END, "⚠️ Enter text to translate"); outputText.config(state=tk.DISABLED); return
        translated = get_translation(txt, from_lang.get(), to_lang.get())
        outputText.config(state=tk.NORMAL); outputText.delete("1.0", tk.END); outputText.insert(tk.END, translated); outputText.config(state=tk.DISABLED)
    except Exception as e: messagebox.showerror("Error", str(e))

def clear_text():
    inputTextEntry.delete("1.0", tk.END)
    outputText.config(state=tk.NORMAL); outputText.delete("1.0", tk.END); outputText.config(state=tk.DISABLED)

def set_lang(var, lang, frame):
    var.set(lang)
    for btn in frame.winfo_children():
        btn.config(bg=COL_INPUT if btn["text"] != lang else COL_PRIMARY,
                   fg="white" if btn["text"] == lang else COL_TEXT)

# Main window
root = tk.Tk()
root.title("🌐 Translator")
root.geometry("540x700")
root.configure(bg="#F9FAFB")

# Styles and colors
FONT_MAIN = ("Segoe UI", 12)
FONT_HEAD = ("Segoe UI", 24)
COL_BG = "#F9FAFB"
COL_CARD = "#FFFFFF"
COL_INPUT = "#FFFFFF"
COL_PRIMARY = "#4F46E5"
COL_SECONDARY = "#9CA3AF"
COL_TEXT = "#111827"

# Main card (now using pack)
card = tk.Frame(root, bg=COL_CARD)
card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Header
tk.Label(card, text="🌐 AI Translator", font=FONT_HEAD, bg=COL_CARD, fg=COL_PRIMARY).pack(pady=(25, 10))

# Language selection
from_lang = tk.StringVar(value="English")
to_lang = tk.StringVar(value="Hindi")
langs = ["English", "Hindi", "French", "Spanish", "Telugu", "Arabic", "Japanese"]

for title, var, default in [("From Language", from_lang, "English"), ("To Language", to_lang, "Hindi")]:
    ttk.Label(card, text=title).pack(anchor="w", padx=30, pady=(4, 0))
    frame = tk.Frame(card, bg=COL_CARD)
    frame.pack(fill="x", padx=30, pady=(0, 15))
    for lang in langs:
        btn = tk.Button(frame, text=lang, bg=COL_INPUT, fg=COL_TEXT, font=FONT_MAIN, relief="solid",
                        command=lambda l=lang, v=var, f=frame: set_lang(v, l, f))
        btn.pack(side="left", padx=2, pady=2)
    set_lang(var, default, frame)  # Set initial selection

# Input/Output
ttk.Label(card, text="✍️ Enter Text").pack(anchor="w", padx=30)
inputTextEntry = tk.Text(card, height=5, bg=COL_INPUT, fg=COL_TEXT, font=FONT_MAIN, padx=10, pady=10, wrap="word")
inputTextEntry.pack(fill="x", padx=30, pady=(5,15))

ttk.Label(card, text="📄 Translation").pack(anchor="w", padx=30)
outputText = tk.Text(card, height=5, bg=COL_INPUT, fg=COL_TEXT, font=FONT_MAIN, padx=10, pady=10, wrap="word")
outputText.pack(fill="x", padx=30, pady=(5,15))
outputText.config(state=tk.DISABLED)

# Buttons
btn_frame = tk.Frame(card, bg=COL_CARD)
btn_frame.pack(fill="x", padx=30, pady=(5,10))
tk.Button(btn_frame, text="🔁 Translate", font=FONT_MAIN, bg=COL_PRIMARY, fg="white", command=translate).pack(side="left", expand=True, fill="x", padx=(0,8))
tk.Button(btn_frame, text="🧹 Clear", font=FONT_MAIN, bg=COL_SECONDARY, fg="white", command=clear_text).pack(side="right", expand=True, fill="x", padx=(8,0))

# Footer
tk.Label(root, text="✨ Powered by AI ✨", font=("Segoe UI", 10), bg=COL_BG, fg=COL_SECONDARY).place(relx=0.5, rely=0.95, anchor=tk.CENTER)

root.mainloop()
