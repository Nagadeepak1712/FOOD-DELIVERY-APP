import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # For image handling
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.chat.util import Chat, reflections

# Sample Data
FOOD_ITEMS = [
    "Pizza", "Burger", "Pasta", "Sushi", "Tacos", "Pancakes", "Waffles", "Ramen", "Burritos", "Salad",
]
DESSERTS = [
    "Chocolate Cake", "Cheesecake", "Brownies", "Apple Pie", "Tiramisu", "Lemon Tart", "Crème Brûlée",
]
JUICES = [
    "Orange Juice", "Apple Juice", "Grape Juice", "Pineapple Juice", "Mango Juice", "Cranberry Juice",
]

# AI Models and Functions
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(FOOD_ITEMS + DESSERTS + JUICES)
y = np.arange(len(FOOD_ITEMS + DESSERTS + JUICES))

clf = MultinomialNB()
clf.fit(X, y)

def predict(text):
    X_test = vectorizer.transform([text])
    return clf.predict(X_test)[0]

def recommend(text):
    if "dessert" in text.lower():
        return "We recommend trying our Chocolate Cake or Cheesecake."
    elif "juice" in text.lower():
        return "How about our Fresh Orange Juice or Green Juice?"
    else:
        return "Here are some recommendations: Pizza, Burger, Dessert, Juice."

pairs = [
    (r"hi|hello", ["Hello! How can I help you today?"]),
    (r"what is your name?", ["I am your food delivery assistant."]),
    (r"(.*) recommend (.*)", [recommend]),
    (r"order (.*)", ["I can help you with placing an order for %1."]),
    (r"bye", ["Goodbye! Have a great day!"]),
]

chatbot = Chat(pairs, reflections)

def get_response(user_input):
    return chatbot.respond(user_input)

# GUI Implementation
def open_login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.configure(bg="lightblue")
    
    tk.Label(login_window, text="Username", bg="lightblue", fg="black").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)
    
    tk.Label(login_window, text="Password", bg="lightblue", fg="black").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    
    tk.Button(login_window, text="Login", command=lambda: login(username_entry.get(), password_entry.get()), bg="green", fg="white").pack(pady=10)

def login(username, password):
    if username and password:
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showwarning("Login", "Please enter both username and password.")

def search():
    search_text = search_entry.get()
    prediction = predict(search_text)
    result_label.config(text=f"Prediction: {prediction}")

def recommend_restaurant():
    user_input = search_entry.get()  # Get input from the search entry
    recommendation = recommend(user_input)
    rec_label.config(text=f"Recommended: {recommendation}")

def chatbot_response():
    user_input = chat_entry.get()
    response = get_response(user_input)
    chat_response_label.config(text=response)

def scroll_left():
    canvas.xview_scroll(-1, "units")

def scroll_right():
    canvas.xview_scroll(1, "units")

def update_slider_label(val):
    slider_label.config(text=f"Quantity: {val}")

def update_progress():
    for i in range(101):
        progress_bar['value'] = i
        root.update_idletasks()
        time.sleep(0.05)

root = tk.Tk()
root.title("Food Delivery App")
root.geometry("1200x800")  # Increased window size for better layout
root.configure(bg="lightblue")

# Logo Section
logo_frame = tk.Frame(root, bg="lightblue")
logo_frame.pack(fill=tk.X, pady=10)

# Add the logo with a large font and color
tk.Label(logo_frame, text="Naggy", font=("Helvetica", 36, "bold"), bg="lightblue", fg="#FFA500").pack()

# Top section with login button
top_frame = tk.Frame(root, bg="lightblue")
top_frame.pack(fill=tk.X, pady=10)

tk.Button(top_frame, text="Login", command=open_login, bg="green", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Main content
main_frame = tk.Frame(root, bg="lightblue")
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Search Box
search_frame = tk.Frame(main_frame, bg="lightblue")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search for a dish:", bg="lightblue", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
search_entry = tk.Entry(search_frame, bg="white", fg="black")
search_entry.pack(side=tk.LEFT, padx=10)
tk.Button(search_frame, text="Search", command=search, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=10)
result_label = tk.Label(main_frame, text="", bg="lightblue", fg="black", font=("Helvetica", 12))
result_label.pack(pady=10)

# Recommendations
recommendation_frame = tk.Frame(main_frame, bg="lightblue")
recommendation_frame.pack(pady=10)

tk.Button(recommendation_frame, text="Recommend Restaurant", command=recommend_restaurant, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)
rec_label = tk.Label(recommendation_frame, text="", bg="lightblue", fg="black", font=("Helvetica", 12))
rec_label.pack(pady=10)

# Chatbot
chatbot_frame = tk.Frame(main_frame, bg="lightblue")
chatbot_frame.pack(pady=10)

tk.Label(chatbot_frame, text="Chat with bot:", bg="lightblue", fg="black", font=("Helvetica", 12)).pack(pady=5)
chat_entry = tk.Entry(chatbot_frame, bg="white", fg="black")
chat_entry.pack(pady=5)
tk.Button(chatbot_frame, text="Send", command=chatbot_response, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
chat_response_label = tk.Label(chatbot_frame, text="", bg="lightblue", fg="black", font=("Helvetica", 12))
chat_response_label.pack(pady=5)

# Slider
slider_frame = tk.Frame(main_frame, bg="lightblue")
slider_frame.pack(pady=10)

tk.Label(slider_frame, text="Select quantity:", bg="lightblue", fg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
slider = tk.Scale(slider_frame, from_=1, to=100, orient="horizontal", command=update_slider_label, bg="white", fg="black")
slider.pack(side=tk.LEFT, padx=10)
slider_label = tk.Label(slider_frame, text="Quantity: 1", bg="lightblue", fg="black", font=("Helvetica", 12))
slider_label.pack(side=tk.LEFT, padx=10)

# Progress Bar
progress_frame = tk.Frame(main_frame, bg="lightblue")
progress_frame.pack(pady=10)

tk.Label(progress_frame, text="Progress:", bg="lightblue", fg="black", font=("Helvetica", 12)).pack(pady=5)
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=5)

tk.Button(progress_frame, text="Start Progress", command=update_progress, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Food Dish Photos
photo_frame = tk.Frame(main_frame, bg="lightblue")
photo_frame.pack(expand=True, fill=tk.BOTH)

# Create a canvas for scrolling
canvas = tk.Canvas(photo_frame, bg="lightblue")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(photo_frame, orient="horizontal", command=canvas.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Load sample images (Replace with actual paths to images)
image_paths = [
    "C:/Users/Deepu/Desktop/python/naggy/poster-recipe-alcoholic-mojito-poster-design-mojito-alcoholic-beverage-alongside-recipes-doses-125903622.webp",
    "C:/Users/Deepu/Desktop/python/naggy/feature-Food-Poster-prototype-sideimage.png",
    "C:/Users/Deepu/Desktop/python/naggy/delicious-asian-food-social-media-template_505751-2963.avif",
    "C:/Users/Deepu/Desktop/python/naggy/feature-Food-Poster-prototype-sideimage.png",
    "C:/Users/Deepu/Desktop/python/naggy/af73930379e819701a21e0d2bab7e9ad.jpg"
]

images = []

for path in image_paths:
    try:
        image = Image.open(path)
        image = image.resize((300, 200))  # Resize image to fit the view
        images.append(ImageTk.PhotoImage(image))
    except Exception as e:
        print(f"Error loading image {path}: {e}")

frame = tk.Frame(canvas, bg="lightblue")
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.config(scrollregion=canvas.bbox("all"), xscrollcommand=scrollbar.set)

for img in images:
    tk.Label(frame, image=img, bg="lightblue").pack(side=tk.LEFT, padx=10)

tk.Button(main_frame, text="Scroll Left", command=scroll_left, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(main_frame, text="Scroll Right", command=scroll_right, bg="orange", fg="white", font=("Helvetica", 12, "bold")).pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()
