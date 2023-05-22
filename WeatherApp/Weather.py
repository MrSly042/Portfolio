import tkinter as tk
from PIL import Image, ImageTk
from dotenv import load_dotenv
import os
import requests

load_dotenv('.env')

API_KEY: str = os.getenv('API_KEY')

class Weather_App(tk.Tk):
    def __init__ (self):
        tk.Tk.__init__ (self)
        
        icon = ImageTk.PhotoImage(file = 'icon.jpeg')
        self.back = ImageTk.PhotoImage(file = 'background.jpg')
        height = self.winfo_screenheight() -240
        width = self.winfo_screenwidth() -30
                
        self.geometry(f'{width}x{height}+10-80')
        self.iconphoto(False, icon)        
        self.title("Chibuike's Weather")
        
        self.config(bg= '#cb6ce6')
        self.getweather()
        
        self.create_widgets()
    
    def getweather(self):
        lat = 9.057310
        lon = 7.444340
        
        url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={API_KEY}'
        response = requests.get(url)
        
        self.data = response.json()
        new = self.data["main"]
        
        global max_temp, min_temp, feel
        max_temp = new['temp_max']
        min_temp = new['temp_min']
        
        feel = new['feels_like']
        hum_dim = new['humidity']
        
        temp = new['temp']
        
        if temp >= 30: chosen = 'sun.png'
        elif temp >= 15 and temp < 30: chosen = 'par_cloud.png'
        elif temp >= 5 and temp < 15: chosen = 'overcast.png'
        elif temp >= 0 and temp <= 5: chosen = 'rain.png'
        elif temp >= -5 and temp <= 0: chosen = 'thunder.png'
        elif temp < -5: chosen = 'snow.png'
        
        self.weat_icon = ImageTk.PhotoImage(file = chosen)
        
    def create_widgets(self):
                
        bg_label = tk.Label(self, image=self.back, )
        bg_label.grid(row=0, column=0, columnspan=2, )
        
        temp_frame = tk.Label(self, text=f'MAX_TEMP : {max_temp}ºC\nMIN_TEMP : {min_temp}ºC', 
                              font=('comic sans ms', 26, 'bold'), )
        
        temp_frame.place(x=10, y =10)
        
        displ_frame = tk.Label(self, image=self.weat_icon, font=('comic sans ms', 26, 'bold'), height=200)
        displ_frame.place(x = 1100, y = 10)
        
        feel_frame = tk.Label(self, text=f"FEELS LIKE {min_temp}ºC", font=('comic sans ms', 26, 'bold'))
        feel_frame.place(x = 10, y = 550)
        
        humid_frame = tk.Label(self, text=f'Humidity: {max_temp}', font=('comic sans ms', 26, 'bold'))
        humid_frame.place(x = 1100, y = 550)        


if __name__ == '__main__':
    app = Weather_App()
    app.mainloop()