import tkinter as tk
from tkinter import ttk, messagebox, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import numpy as np

 
class IQTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IQ ARENA")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors and fonts
        self.colors = {
            'background': '#2E3440',
            'primary': '#88C0D0',
            'secondary': '#5E81AC',
            'text': '#2E3440',
            'error': '#D08770'
        }
        self.fonts = {
            'title': ('Helvetica', 20, 'bold'),
            'question': ('Arial', 14),
            'button': ('Arial', 12)
        }
        
        # Style configuration for error messages
        self.style.configure('Error.TLabel', 
                           foreground=self.colors['error'], 
                           font=('Arial', 14, 'bold'))
        
        # Initialize quiz variables
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.responses = []
        self.start_time = 0
        self.scoring_weights = {"Easy": 1, "Medium": 2, "Hard": 3}
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_start_screen()
    
    def load_questions(self):
        return [
            {
               "question": "Which algorithm is used to find the shortest path in a weighted graph with non-negative weights?",
               "options": [
                        "Dijkstra's algorithm",
                        "Bellman-Ford algorithm",
                        "Floyd-Warshall algorithm",
                        "Kruskal's algorithm"
                    ],
                "correct": "Dijkstra's algorithm",
                "difficulty": "Hard"
            },
            {
                "question": "Solve: 3x = 27",
                "options": ["6", "7", "8", "9"],
                "correct": "9",
                "difficulty": "Medium"
            },
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct": "Paris",
                "difficulty": "Easy"
            },
            {
                "question": "Find the next shape in the series: Square, Triangle, Pentagon, __?",
                "options": ["Hexagon", "Heptagon", "Octagon", "Nonagon"],
                "correct": "Heptagon",
                "difficulty": "Hard",
            },
            {
                "question": "Which shape is a triangle?",
                "options": ["triangle.png", "circle.png", "square.png", "hexagon.png"],
                "correct": "triangle.png",
                "difficulty": "Easy",
                "is_image": True 
            },
            {
                "question": "Which is the largest desert in the world?",
                "options": ["Sahara", "Antarctica", "Gobi", "Kalahari"],
                "correct": "Antarctica",
                "difficulty": "Medium",
            }
        ]
    
    def show_start_screen(self):
        self.clear_frame()
        start_frame = ttk.Frame(self.main_frame)
        
        title = ttk.Label(start_frame, text="IQ ARENA", 
                         font=self.fonts['title'],
                         foreground=self.colors['primary'])
        title.pack(pady=20)
        
        start_btn = ttk.Button(start_frame, text="Start Quiz", 
                              command=self.start_quiz)
        start_btn.pack(pady=10)
        
        start_frame.pack(expand=True)
    
    def start_quiz(self):
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.responses = []
        self.show_question()
    
    def show_question(self):
        self.clear_frame()
        question_frame = ttk.Frame(self.main_frame)
        
        # Progress bar
        self.progress = ttk.Progressbar(question_frame, 
                                       orient=tk.HORIZONTAL,
                                       length=600, 
                                       mode='determinate')
        self.progress['value'] = (self.current_question / len(self.questions)) * 100
        self.progress.pack(pady=10)
        
        # Question display
        q_data = self.questions[self.current_question]
        question_text = ttk.Label(question_frame, 
                                 text=q_data["question"],
                                 font=self.fonts['question'], 
                                 wraplength=600)
        question_text.pack(pady=20)

        # Answer buttons
        btn_frame = ttk.Frame(question_frame)
        
        # Check if the question contains images
        if q_data.get("is_image", False):
            self.image_objects = [] 
            for option in q_data["options"]:
                image = Image.open(option) 
                image = image.resize((100, 100)) 
                photo = ImageTk.PhotoImage(image)  
                self.image_objects.append(photo) 
                btn = tk.Button(btn_frame, image=photo, command=lambda o=option: self.check_answer(o))
                btn.pack(side=tk.LEFT, padx=5)  
        else:
            for option in q_data["options"]:
                btn = ttk.Button(btn_frame, text=option, command=lambda o=option: self.check_answer(o))
                btn.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        
        btn_frame.pack()
        question_frame.pack(expand=True)
        self.start_time = time.time()

    
    def check_answer(self, selected_option):
        q_data = self.questions[self.current_question]
        time_taken = time.time() - self.start_time
        is_correct = selected_option == q_data["correct"]
        
        if is_correct:
            self.score += self.scoring_weights[q_data["difficulty"]]
        
        self.responses.append({
            "question": q_data["question"],
            "selected": selected_option,
            "correct": q_data["correct"],
            "difficulty": q_data["difficulty"],
            "time": time_taken,
            "is_correct": is_correct,
            "is_image": q_data.get("is_image", False) 
        })
        
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()
    
    def show_results(self):
        self.clear_frame()
        results_frame = ttk.Frame(self.main_frame)
        all_wrong = all(not resp['is_correct'] for resp in self.responses)
        
        # for all-wrong case
        if all_wrong:
            ttk.Label(results_frame, 
                    text="All Answers Incorrect!",
                    style='Error.TLabel').pack(pady=10)
            
        ttk.Button(results_frame, text="Review Answers",
           command=self.show_review).pack(pady=10)    
        
        # Score display with conditional color
        score_color = self.colors['primary'] if not all_wrong else self.colors['error']
        ttk.Label(results_frame, 
                text=f"Final Score: {self.score}",
                font=self.fonts['title'],
                foreground=score_color).pack(pady=20)
        
        # Analytics section
        analytics_frame = ttk.Frame(results_frame)
        self.display_analytics(analytics_frame, all_wrong)
        analytics_frame.pack(pady=20)
        
        # Visualization section
        viz_frame = ttk.Frame(results_frame)
        self.create_visualizations(viz_frame, all_wrong)
        viz_frame.pack(pady=20)
        
        # Review button
        ttk.Button(results_frame, text="Review Answers",
                 command=self.show_review).pack(pady=2)
        
        results_frame.pack(expand=True)
        results_frame.update_idletasks()
    
    def display_analytics(self, parent, all_wrong=False):
        difficulties = ["Easy", "Medium", "Hard"]
        avg_times = []
        accuracies = []
        
        for diff in difficulties:
            times = [r["time"] for r in self.responses if r["difficulty"] == diff]
            correct = sum(1 for r in self.responses 
                         if r["difficulty"] == diff and r["is_correct"])
            total = len(times)
            
            avg_times.append(np.mean(times) if times else 0)
            accuracies.append((correct / total * 100) if total else 0)
        
        # Display metrics
        if all_wrong:
            ttk.Label(parent, 
                    text="Analysis: No correct answers in any difficulty level",
                    style='Error.TLabel').pack(pady=10)
        else:
            ttk.Label(parent, text="Performance Analysis:").pack()
        
        for i, diff in enumerate(difficulties):
            fg = self.colors['text'] if accuracies[i] > 0 else self.colors['error']
            ttk.Label(parent, 
                     text=f"{diff}: Avg Time {avg_times[i]:.1f}s, Accuracy {accuracies[i]:.1f}%",
                     foreground=fg).pack()
    
    def create_visualizations(self, parent, all_wrong=False):
        fig = plt.figure(figsize=(12, 5))
        gs = fig.add_gridspec(1, 3)
        
        # Average Response Times (Left)
        ax1 = fig.add_subplot(gs[0, 0])
        difficulties = ["Easy", "Medium", "Hard"]
        avg_times = [np.mean([r["time"] for r in self.responses if r["difficulty"] == diff]) 
                   for diff in difficulties]
        ax1.bar(difficulties, avg_times, color=self.colors['secondary'])
        ax1.set_title("Average Response Times")
        ax1.set_ylabel("Seconds")
        ax1.set_xlabel("Difficulty Level")
        
        # Accuracy Pie Chart (Middle)
        ax2 = fig.add_subplot(gs[0, 1])
        correct = [sum(1 for r in self.responses 
                      if r["difficulty"] == diff and r["is_correct"])
                  for diff in difficulties]
        
        if all_wrong:
            ax2.text(0.5, 0.5, 'No\nCorrect\nAnswers', 
                    ha='center', va='center', fontsize=16)
            ax2.set_title("Accuracy Overview")
        else:
            ax2.pie(correct, labels=difficulties, autopct='%1.1f%%',
                   colors=[self.colors['primary'], self.colors['secondary'], '#5E81AC'])
            ax2.set_title("Correct Answers by Difficulty")
        
        # Time Per Question 
        ax3 = fig.add_subplot(gs[0, 2])
        question_numbers = [f"Q{i+1}" for i in range(len(self.responses))]
        times = [r["time"] for r in self.responses]
        bar_color = self.colors['primary'] if not all_wrong else self.colors['error']
        bars = ax3.bar(question_numbers, times, color=bar_color)
        
        # Add time labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}s',
                    ha='center', va='bottom', fontsize=8)
        
        ax3.set_title("Time Taken Per Question")
        ax3.set_ylabel("Seconds")
        ax3.set_xlabel("Questions")
        ax3.set_xticks(range(len(question_numbers)))  
        ax3.set_xticklabels(question_numbers, rotation=0, ha='right')  
        plt.subplots_adjust(left=0.15, right=0.95, bottom=0.2, top=0.9)  
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def show_review(self):
        review_win = tk.Toplevel(self.root)
        review_win.title("Answer Review")

        review_win.geometry("500x500")
        review_win.resizable(False, False) # Disable resizing
        all_wrong = all(not resp['is_correct'] for resp in self.responses)
        
        if all_wrong:
            ttk.Label(review_win, text="All Answers Were Incorrect",
                     style='Error.TLabel').pack(pady=10)
        
        canvas = Canvas(review_win)
        scrollbar = ttk.Scrollbar(review_win, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.review_images = [] 
        
        for idx, response in enumerate(self.responses):
            frame = ttk.Frame(scrollable_frame, padding=10)
            text_color = 'green' if response['is_correct'] else 'red'
            
            # Display Question
            ttk.Label(frame, text=f"Question {idx+1}: {response['question']}", wraplength=600).pack(anchor='w')

            if "is_image" in response and response["is_image"]:
                # Display Selected Answer Image
                selected_image = Image.open(response["selected"])
                selected_image = selected_image.resize((100, 100))  
                selected_photo = ImageTk.PhotoImage(selected_image)
                self.review_images.append(selected_photo)
                
                ttk.Label(frame, text="Your Answer:", foreground=text_color).pack(anchor='w')
                ttk.Label(frame, image=selected_photo).pack(anchor='w')

                # Display Correct Answer Image
                correct_image = Image.open(response["correct"])
                correct_image = correct_image.resize((100, 100))  
                correct_photo = ImageTk.PhotoImage(correct_image)
                self.review_images.append(correct_photo)
                
                ttk.Label(frame, text="Correct Answer:", foreground='blue').pack(anchor='w')
                ttk.Label(frame, image=correct_photo).pack(anchor='w')

            else:
                # Display Text Answers
                ttk.Label(frame, text=f"Your Answer: {response['selected']}", foreground=text_color).pack(anchor='w')
                ttk.Label(frame, text=f"Correct Answer: {response['correct']}", foreground='blue').pack(anchor='w')

            ttk.Label(frame, text=f"Time Taken: {response['time']:.1f}s").pack(anchor='w')
            frame.pack(fill=tk.X, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IQTestApp(root)
    root.mainloop()