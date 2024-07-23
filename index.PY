import tkinter as tk
from tkinter import messagebox
import sqlite3

class VotingWindow:
    def __init__(self, master, candidate_names):
        self.master = master
        self.master.title("Voting Window")
        self.connection = sqlite3.connect('votes.db')
        self.cursor = self.connection.cursor()
        self.create_table()

        self.candidate_names = candidate_names
        self.create_widgets()
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            votes INTEGER)''')
        self.connection.commit()

    def create_widgets(self):
        self.vote_buttons = []

        for i, name in enumerate(self.candidate_names):
            label = tk.Label(self.master, text=name)
            label.grid(row=i, column=0, padx=10, pady=5)
            vote_button = tk.Button(self.master, text="Vote", command=lambda name=name: self.cast_vote(name))
            vote_button.grid(row=i, column=1, padx=10, pady=5)
            self.vote_buttons.append(vote_button)

        self.results_button = tk.Button(self.master, text="Show Results", command=self.show_results)
        self.results_button.grid(row=len(self.candidate_names), column=0, padx=10, pady=10)

        self.clear_button = tk.Button(self.master, text="Clear Votes", command=self.clear_votes)
        self.clear_button.grid(row=len(self.candidate_names), column=1, padx=10, pady=10)

    def cast_vote(self, candidate_name):
        self.cursor.execute("SELECT * FROM candidates WHERE name=?", (candidate_name,))
        candidate = self.cursor.fetchone()
        if candidate:
            self.cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE name=?", (candidate_name,))
        else:
            self.cursor.execute("INSERT INTO candidates (name, votes) VALUES (?, 1)", (candidate_name,))
        self.connection.commit()
        messagebox.showinfo("Success", "Your vote has been cast successfully!")
        for button in self.vote_buttons:
            button.config(state=tk.DISABLED)

    def show_results(self):
        self.cursor.execute("SELECT * FROM candidates")
        results = self.cursor.fetchall()
        if results:
            result_text = "Candidate\tVotes\n"
            for row in results:
                result_text += f"{row[1]}\t\t{row[2]}\n"
            messagebox.showinfo("Election Results", result_text)
        else:
            messagebox.showwarning("Warning", "No candidates available.")

    def clear_votes(self):
        confirmation = messagebox.askyesno("Clear Votes", "Are you sure you want to clear all votes?")
        if confirmation:
            self.cursor.execute("DELETE FROM candidates")
            self.connection.commit()
            messagebox.showinfo("Success", "All votes have been cleared!")

class OnlineElectionSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Online Election System")
        
        self.connection = sqlite3.connect('votes.db')
        self.cursor = self.connection.cursor()
        self.create_table()

        self.create_widgets()
        
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            votes INTEGER)''')
        self.connection.commit()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Enter the number of persons participating in the election:")
        self.label.pack()

        self.persons_entry = tk.Entry(self.master)
        self.persons_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.create_name_entries)
        self.submit_button.pack()

        self.results_button = tk.Button(self.master, text="Show Results", command=self.show_results)
        self.results_button.pack()

        self.clear_button = tk.Button(self.master, text="Clear Votes", command=self.clear_votes)
        self.clear_button.pack()

    def create_name_entries(self):
        num_persons = int(self.persons_entry.get())
        self.persons_entry.destroy()
        self.submit_button.destroy()

        self.name_entries = []

        for i in range(num_persons):
            label = tk.Label(self.master, text=f"Enter name of Person {i+1}:")
            label.pack()
            name_entry = tk.Entry(self.master)
            name_entry.pack()
            self.name_entries.append(name_entry)

        self.submit_names_button = tk.Button(self.master, text="Submit Names", command=self.open_voting_window)
        self.submit_names_button.pack()

    def open_voting_window(self):
        candidate_names = [entry.get() for entry in self.name_entries if entry.get()]
        if candidate_names:
            voting_window = tk.Toplevel(self.master)
            voting_window.geometry("300x200")
            VotingWindow(voting_window, candidate_names)
        else:
            messagebox.showwarning("Warning", "Please enter all candidates' names.")

    def show_results(self):
        self.cursor.execute("SELECT * FROM candidates")
        results = self.cursor.fetchall()
        if results:
            result_text = "Candidate\tVotes\n"
            for row in results:
                result_text += f"{row[1]}\t\t{row[2]}\n"
            messagebox.showinfo("Election Results", result_text)
        else:
            messagebox.showwarning("Warning", "No candidates available.")

    def clear_votes(self):
        confirmation = messagebox.askyesno("Clear Votes", "Are you sure you want to clear all votes?")
        if confirmation:
            self.cursor.execute("DELETE FROM candidates")
            self.connection.commit()
            messagebox.showinfo("Success", "All votes have been cleared!")

def main():
    root = tk.Tk()
    app = OnlineElectionSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
