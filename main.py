import tkinter as tk
from tkinter import messagebox, filedialog
from zxcvbn import zxcvbn
import requests
import hashlib
import math

# Calculating Entropy Values
def calculate_entropy(password):
    length = len(password)
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    if charset == 0:
        return 0

    entropy = length * math.log2(charset)
    return entropy


def evaluate_password(event=None):
    password = entry.get()

    if password == hint_text:
        password = ""

    if not password:
        entry.config(bg="white")
        return

    result = zxcvbn(password)
    score = result['score']

    suggestions = result['feedback']['suggestions']
    warning = result['feedback']['warning']
    crack_times = result['crack_times_display']

    strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    strength_message = strength_levels[score]

    suggestions_text = "\n".join(suggestions) if suggestions else "No suggestions, the password is strong."

    crack_time_message = f"""
Offline Fast Hashing (1e10/s): {crack_times['offline_fast_hashing_1e10_per_second']}
Offline Slow Hashing (1e4/s): {crack_times['offline_slow_hashing_1e4_per_second']}
Online No Throttling (10/s): {crack_times['online_no_throttling_10_per_second']}
Online Throttling (100/h): {crack_times['online_throttling_100_per_hour']}
"""

    # Have I Been Pwned Check
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            pwned_count = next((int(count) for h, count in hashes if h == suffix), 0)
            if pwned_count > 0:
                pwned_message = f"\n\nWarning: Found in {pwned_count} breaches!"
            else:
                pwned_message = "\n\nGood news: Not found in breaches."
        else:
            pwned_message = "\n\nCould not check breach database."
    except requests.RequestException:
        pwned_message = "\n\nCould not check breach database."

    entropy = calculate_entropy(password)
    entropy_message = f"Entropy: {entropy:.2f} bits"

    result_message = f"""
Password: {password}

Password Strength: {strength_message}

Warning: {warning}

Suggestions:
{suggestions_text}

Time to Crack:
{crack_time_message}

{entropy_message}

{pwned_message}
"""

    messagebox.showinfo("Password Strength Checker", result_message)

    # Visual Color Feedback
    colors = ["red", "orange", "yellow", "lightgreen", "green"]
    entry.config(bg=colors[score])

    return result_message


def save_report():
    result_message = evaluate_password()
    if not result_message:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", ".txt"), ("All files", ".*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(result_message)
        messagebox.showinfo("Save Report", "Report saved successfully!")


def show_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        eye_button.config(text="Hide")
    else:
        entry.config(show='*')
        eye_button.config(text="Show")


def clear_hint(event):
    if entry.get() == hint_text:
        entry.delete(0, tk.END)
        entry.config(fg='black', show='*')


def set_hint(event):
    if not entry.get():
        entry.insert(0, hint_text)
        entry.config(fg='grey', show='')


# GUI Setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x400")

center_frame = tk.Frame(root, bg="#000", bd=10, relief=tk.RAISED)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(center_frame, text="Password Strength Checker",
                       font=("Times New Roman", 18), fg="white", bg="#000")
title_label.pack(pady=10)

hint_text = "Enter your password"

entry_frame = tk.Frame(center_frame, bg="#808080")
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=20, font=("Times New Roman", 16), fg='grey', bg="white")
entry.insert(0, hint_text)
entry.pack(side=tk.LEFT, padx=5)

entry.bind("<FocusIn>", clear_hint)
entry.bind("<FocusOut>", set_hint)
entry.bind("<Return>", evaluate_password)

eye_button = tk.Button(entry_frame, text="Show", command=show_password, bg="#808080")
eye_button.pack(side=tk.RIGHT)

check_button = tk.Button(center_frame, text="Check Password Strength",
                         command=evaluate_password, font=("Times New Roman", 14))
check_button.pack(pady=10)

save_button = tk.Button(center_frame, text="Save Report",
                        command=save_report, font=("Times New Roman", 14))
save_button.pack(pady=10)

root.mainloop()

