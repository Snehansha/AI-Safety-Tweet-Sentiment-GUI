import tkinter as tk
from tkinter import ttk, messagebox
from textblob import TextBlob
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Load and analyze tweets
def analyze_tweets():
    try:
        df = pd.read_csv("sample_tweets.csv", encoding="latin-1")
        df['sentiment'] = df['text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        
        df['label'] = df['sentiment'].apply(
            lambda score: 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'
        )

        pos_count = (df['label'] == 'Positive').sum()
        neg_count = (df['label'] == 'Negative').sum()
        neu_count = (df['label'] == 'Neutral').sum()
        total = len(df)

        # Update labels
        total_label.config(text=f"Total Tweets Analyzed: {total}")
        pos_label.config(text=f"Positive: {pos_count}")
        neg_label.config(text=f"Negative: {neg_count}")
        neu_label.config(text=f"Neutral: {neu_count}")

        # Show top 5 analyzed tweets
        top5 = df[['text', 'sentiment']].head(5)
        text_area.delete(1.0, tk.END)
        for index, row in top5.iterrows():
            text_area.insert(tk.END, f"{index+1}. {row['text'][:100]}...\n   Sentiment Score: {row['sentiment']:.2f}\n\n")

        # Pie chart
        plot_pie_chart(pos_count, neg_count, neu_count)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze tweets.\n{e}")

# Draw pie chart
def plot_pie_chart(pos, neg, neu):
    fig, ax = plt.subplots(figsize=(4, 4))
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [pos, neg, neu]
    colors = ['lightgreen', 'salmon', 'lightblue']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title("Sentiment Distribution")

    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Tkinter GUI
root = tk.Tk()
root.title("AI Tweet Sentiment Analyzer")
root.geometry("800x600")
root.resizable(False, False)

ttk.Label(root, text="📊 Tweet Sentiment Analysis", font=("Segoe UI", 18, "bold")).pack(pady=10)

# Stats labels
total_label = ttk.Label(root, text="Total Tweets Analyzed: 0", font=("Segoe UI", 12))
total_label.pack()

pos_label = ttk.Label(root, text="Positive: 0", font=("Segoe UI", 12))
pos_label.pack()

neg_label = ttk.Label(root, text="Negative: 0", font=("Segoe UI", 12))
neg_label.pack()

neu_label = ttk.Label(root, text="Neutral: 0", font=("Segoe UI", 12))
neu_label.pack()

# Chart and tweets
chart_frame = ttk.Frame(root)
chart_frame.pack(side=tk.LEFT, padx=20, pady=20)

text_area = tk.Text(root, width=50, height=20, font=("Segoe UI", 10))
text_area.pack(side=tk.RIGHT, padx=10, pady=20)

# Auto-run analysis on start
analyze_tweets()

root.mainloop()
