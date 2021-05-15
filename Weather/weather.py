"""Application Design."""
import sys
sys.path.insert(0, '..')
import tkinter as tk
from tkinter import ttk
from skeleton import Application
import requests
import datetime

from io import BytesIO
from PIL import Image, ImageTk


class weather_day(tk.Frame):

    def __init__(self, master=None, date='', icon_num='', temp='', descrip='', **kw):
        super().__init__(master=master, **kw)
        self.date = date
        self.icon_num = icon_num
        self.temp = temp
        self.description = descrip
        self.create_widgets()

    def create_widgets(self):
        """Widgets creation."""

        self.day = tk.Label(self, justify="center", text=self.date, width=33)
        self.day.grid(row=0, column=0, sticky="NEWS")

        self.icon = tk.Label(self, text="No Icon Yet", justify="center", width=33)
        self.icon.grid(row=1, column=0, sticky="NEWS")

        self.descript = tk.Label(self, text=self.description, justify="center", width=33)
        self.descript.grid(row=2, column=0, sticky="NEWS")

        self.temperature = tk.Label(self, text=self.temp, justify="center", width=33)
        self.temperature.grid(row=3, column=0, sticky="NEWS")

        self.link = "http://openweathermap.org/img/wn/"

        self.load_icon(self.link+self.icon_num+".png")


    def load_icon(self, url):
        self.icon['text'] = 'Loading picture...'
        self.update()
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            self.icon['text'] = 'Timeout error'
        else:
            if response.status_code != 200:
                self.icon['text'] = 'HTTP error ' + str(response.status_code)
            else:
                pil_image = Image.open(BytesIO(response.content))
                image = ImageTk.PhotoImage(pil_image)
                self.icon.config(image=image, text='')
                self.icon.image = image

class WeatherApp(Application):
    """Sample Application."""

    def __init__(self, master=None, mainm=None, **kw):
        super().__init__(master=master, **kw)
        master.minsize(800, 400)
        master.maxsize(1000, 500)
        self.back = mainm
        self.create_widgets()


    def create_widgets(self):
        """Widgets creation."""

        self.appid = tk.StringVar()
        self.appid.set("d83a96348dfb13f8e92f0ae8929e1eff")

        self.city_id = 0

        self.city = tk.StringVar()
        self.city.set('Tver')

        self.units = tk.StringVar()
        self.units.set('metric')

        self.lang = tk.StringVar()
        self.lang.set('en')

        self.find_city()

        self.days = ['']

        self.weatherButton = tk.Button(self, text="Weather for now!", command=self.getweather)
        self.weatherButton.grid(row=1, column=0, sticky="NEWS")

        #self.forecastButton = tk.Button(self, text="Forecast!", command=self.forecast)
        #self.forecastButton.grid(row=2, column=0, sticky="NEWS")

        self.weathers = ttk.Notebook(self)
        self.weathers.grid(row=3, column=0, sticky="NEWS")

        self.three_days = ttk.Frame(self.weathers, width=300, height=200)
        self.five_days = ttk.Frame(self.weathers, width=300, height=200)

        self.weathers.add(self.three_days, text="3 days")
        self.weathers.add(self.five_days, text="5 days")

        now_date = datetime.datetime.now()
        forcst = self.forecast()

        for day in forcst:
            current_date = datetime.datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S")
            diff = datetime.timedelta(hours=1,minutes=30)
            weather_descript = day['weather'][0]['description']
            temperature = day['main']['temp']
            icon = day['weather'][0]['icon']
            diction = {'date': current_date, 'description': weather_descript, 'temp':temperature, 'icon':icon}
            if (abs(current_date-now_date) < diff):
                print(diction)
                self.days[0] = diction
            elif (current_date.hour==12 and current_date.day != now_date.day):
                print(diction)
                if (diction not in self.days):
                    self.days.append(diction)
            #print(current_date)
            #date = day['dt_txt']
            #print('{a}: {b}: {c} {d}'.format(a=current_date, b=weather_descript, c=temperature, d=icon))


        self.three_days_list = []
        for i in range(3):
            new_day = self.days[i]
            self.three_days_list.append('')
            self.three_days_list[i] = weather_day(master=self.three_days,
                                                  icon_num=new_day['icon'], temp=new_day['temp'],
                                                  date=new_day['date'], descrip=new_day['description'])
            self.three_days_list[i].grid(row=0, column=i, sticky="NEWS")

        self.five_days_list = []
        for i in range(5):
            self.five_days_list.append('')
            self.five_days_list[i] = weather_day(master=self.five_days)
            self.five_days_list[i].grid(row=0, column=i, sticky="NEWS")

        self.link = "http://openweathermap.org/img/wn/"

        #self.load_icon(self.link+"10d@4x.png")

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Kill me!")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Settings", command=self.settings)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Go to Main Menu", command=self.go_back)
        self.filemenu.add_command(label="Close", command=self.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        self.master.config(menu=self.menubar)

        #self.find_city()
        #self.getweather()
        #self.forecast()

    def settings(self):

        def on_closing():
            if tk.messagebox.askyesno("Quit", "Do you want to quit?\nTo save your reminder, you have to press OK"):
                top.destroy()

        top = tk.Toplevel(self)
        top.resizable(False, False)
        top.protocol("WM_DELETE_WINDOW", on_closing)
        top.focus_set()
        top.grab_set()

        old_city = self.city.get()

        tim_lab = tk.Label(top, text="API:")
        tim_lab.grid(row=0, column=0, sticky="NEWS", columnspan=4, ipady=10, pady=5, padx=5)

        API_entry = tk.Entry(top, textvariable=self.appid, width=35, justify='center')
        API_entry.grid(row=0, column=4, sticky="NEWS", ipady=10, pady=5, columnspan=2)

        tim_lab = tk.Label(top, text="Language:")
        tim_lab.grid(row=1, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        lang_entry = tk.Entry(top, textvariable=self.lang, width=10, justify='center')
        lang_entry.grid(row=1, column=4, sticky="NEWS", ipady=5, pady=5, columnspan=2)

        tim_lab = tk.Label(top, text="City:")
        tim_lab.grid(row=2, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        city_entry = tk.Entry(top, textvariable=self.city, width=10, justify='center')
        city_entry.grid(row=2, column=4, sticky="NEWS", ipady=5, pady=5, columnspan=2)

        unit_label = tk.Label(top, text='Units:')
        unit_label.grid(row=3, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        metric_unit = tk.Radiobutton(top, text="metric", variable=self.units, value="metric")
        metric_unit.grid(row=3, column=4, sticky="NEWS", ipady=5, pady=5, padx=5)

        imperial_unit = tk.Radiobutton(top, text="imperial", variable=self.units, value="imperial")
        imperial_unit.grid(row=3, column=5, sticky="NEWS", ipady=5, pady=5, padx=5)

        B = tk.Button(top, text="OK", command=top.destroy)
        B.grid(row=4, column=0, columnspan=8, sticky="NEWS", padx=2, pady=2)

        top.wait_window()

        if (old_city != self.city.get()):
            self.find_city()


    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")

    def find_city(self):
        s_city = "Tver"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': self.units.get(), 'APPID': self.appid.get()})
            data = res.json()
            self.city_id = data['list'][0]['id']
        except Exception as e:
            print("Exception (find):", e)
            pass

    def getweather(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': self.city_id, 'units': self.units.get(), 'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            print("temp:", data['main']['temp'])
            print("temp_min:", data['main']['temp_min'])
            print("temp_max:", data['main']['temp_max'])
        except Exception as e:
            print("Exception (weather):", e)
            pass

    def forecast(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'id': self.city_id, 'units': self.units.get(), 'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            return data['list']
            #for i in data['list']:
            #    print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
        except Exception as e:
            print("Exception (forecast):", e)
            pass 
