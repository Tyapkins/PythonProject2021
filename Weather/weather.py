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

    def __init__(self, master=None, max_width=28, date='', icon_num='',
                 temp='', descrip='', extra={}, **kw):
        super().__init__(master=master, **kw)
        self.date = date
        self.icon_num = icon_num
        self.temp = temp
        self.description = descrip
        self.mwidth = max_width
        self.extra_info = extra
        self.create_widgets()

    def create_widgets(self):
        """Widgets creation."""

        actual_name = self.date.strftime("%B, %d,\n%H:%M")

        self.day = tk.Label(self, justify="center", text=actual_name, width=self.mwidth)
        self.day.grid(row=0, column=0, sticky="NEWS")

        self.icon = tk.Label(self, text="No Icon Yet", justify="center", width=self.mwidth)
        self.icon.grid(row=1, column=0, sticky="NEWS")

        self.descript = tk.Label(self, text=self.description, justify="center", width=self.mwidth)
        self.descript.grid(row=2, column=0, sticky="NEWS")

        self.temperature = tk.Label(self, text=self.temp, justify="center", width=self.mwidth)
        self.temperature.grid(row=3, column=0, sticky="NEWS")

        self.extra = tk.Label(self, justify="center", width=self.mwidth)
        self.extra.grid(row=4, column=0, sticky="NEWS")

        if len(self.extra_info) > 0:
            self.fill_extra()

        self.link = "http://openweathermap.org/img/wn/"

        self.load_icon(self.link+self.icon_num+".png")

    def deg_to_dir(self, angle):
        dirs = ['↑ N', '↗ NNE', '↗ NE', '↗ ENE', '→ E', '↘ ESE', '↘ SE', '↘ SSE', '↓ S', '↙ SSW', '↙ SW', '↙ WSW', '← W', '↖ WNW', '↖ NW', '↖ NNW']
        ix = round(angle/(360. / len(dirs)))
        return dirs[ix % len(dirs)]

    def fill_extra(self):
        self.extra['text'] = ''
        for info in self.extra_info:
            if (info != 'wind'):
                extra_info = ''
                if self.temperature['text'][-1] == "C" or self.temperature['text'][-1] == "K":
                    measurement = "%" if (info == "Air Humidity") \
                        else ("°"+self.temperature['text'][-1] if (info == "Temperature feels like") else
                              "hPa" if (info == "Atmosphere Pressure") else '')
                else:
                    measurement = "%" if (info == "Air Humidity") \
                        else ("°F" if (info == "Temperature feels like") else
                              "hPa" if (info == "Atmosphere Pressure") else '')
                self.extra['text'] += "{a}: {b} {c},\n".format(a=info, b=self.extra_info[info], c=measurement)
            else:
                self.extra['text'] += "{a}: {b} {s},\n{c}: {d}".format(a="Wind Speed", b=self.extra_info['wind']['speed'],
                                                                   c="Wind Direction",
                                                                   d=self.deg_to_dir(self.extra_info['wind']['deg']),
                                                                   s="m/s" if self.temperature['text'][-1] == "C" else "mp/h"
                                                                       )


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
        master.minsize(1150, 850)
        master.maxsize(1200, 900)
        super().__init__(master=master, **kw)
        self.back = mainm
        #self.create_widgets()


    def create_widgets(self):
        """Widgets creation."""
        self.appid = tk.StringVar()
        self.city_id = 0
        self.city = tk.StringVar()
        self.units = tk.StringVar()

        self.grad = " °C"

        self.details = tk.IntVar()
        self.lang = tk.StringVar()
        self.defaults()

        self.days = ['']


        self.weatherButton = tk.Button(self, text="Weather in a moment", command=self.weather_now_update)
        self.weatherButton.grid(row=1, column=0, sticky="NEWS", rowspan=2)

        self.weather_now()

        self.separ = ttk.Separator(self, orient='horizontal')
        self.separ.grid(row=3, column=0, columnspan=4, sticky="WE", pady=5, ipady=5)


        self.weathers = ttk.Notebook(self)
        self.weathers.grid(row=4, column=0, sticky="NEWS", columnspan=2)

        self.three_days = ttk.Frame(self.weathers, width=300, height=200)
        self.five_days = ttk.Frame(self.weathers, width=300, height=200)

        self.weathers.add(self.three_days, text="3 days")
        self.weathers.add(self.five_days, text="5 days")

        now_date = datetime.datetime.now()
        forcst = self.forecast()

        for day in forcst:
            current_date = datetime.datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S")
            diff = datetime.timedelta(hours=1, minutes=30)
            diction=self.make_day(day)
            if (abs(current_date-now_date) < diff):
                self.days[0] = diction
            elif (current_date.hour==12 and current_date.day != now_date.day):
                if (diction not in self.days):
                    self.days.append(diction)

        self.three_days_list = []
        self.three_buttons = []
        self.fill_mas(self.three_days_list, self.three_buttons, self.three_days, 47, 3)

        self.five_days_list = []
        self.five_buttons = []
        self.fill_mas(self.five_days_list, self.five_buttons, self.five_days, 28, 5)

        self.link = "http://openweathermap.org/img/wn/"

        #self.load_icon(self.link+"10d@4x.png")

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Settings", command=self.settings)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Go to Main Menu", command=self.go_back)
        self.filemenu.add_command(label="Close", command=self.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        self.master.config(menu=self.menubar)

    def defaults(self):
        self.appid.set("d83a96348dfb13f8e92f0ae8929e1eff")
        self.city.set('Tver')
        self.units.set('metric')
        self.grad = " °C"
        self.details.set(0)
        self.lang.set('en')
        self.find_city()

    def weather_now(self):
        day = self.make_day(self.getweather())
        extra_info = day['extra'] if self.details.get() != 0 else {}
        self.wnow = weather_day(master=self,
                                icon_num=day['icon']+"@4x",
                                temp=str(day['temp'])+self.grad,
                                date=day['date'], descrip=day['description'],
                                extra=extra_info)
        self.wnow.grid(row=1, column=1, rowspan=2)

    def weather_now_update(self):
        self.check_changes(self.wnow, self.getweather())



    def fill_mas(self, mas, buttons, tab, section_width, max_size):
        for i in range(max_size):
            new_day = self.days[i]
            mas.append('')
            extra_info = new_day['extra'] if self.details.get() != 0 else {}
            mas[i] = weather_day(master=tab, max_width=section_width,
                                                  icon_num=new_day['icon']+"@4x",
                                                  temp=str(new_day['temp'])+self.grad,
                                                  date=new_day['date'], descrip=new_day['description'],
                                                  extra=extra_info)
            mas[i].grid(row=0, column=i, sticky="NEWS")

            buttons.append('')
            buttons[i] = tk.Button(master=tab,
                                    command=(lambda x=new_day['date'].day: self.more(x)),
                                    text="More Information")
            buttons[i].grid(row=1, column=i, sticky="NEWS")

    def more(self, day_num):

        def day_weather():
            mas = self.forecast()
            final_mas = []
            for day in mas:
                true_day = self.make_day(day)
                if (true_day['date'].day == day_num):
                    final_mas.append(true_day)

            top = tk.Toplevel(self)
            top.resizable(False, False)
            top.focus_set()
            top.grab_set()

            mas_days = []
            #print(self)

            for i in range(len(final_mas)):
                new_day = final_mas[i]
                mas_days.append('')
                extra_info = final_mas[i]['extra'] if self.details.get() != 0 else {}
                mas_days[i] = weather_day(top, icon_num=new_day['icon']+"@2x",
                                            temp=str(new_day['temp'])+self.grad,
                                            date=new_day['date'],
                                            descrip=new_day['description'],
                                            extra=extra_info,
                                            max_width=40)
                mas_days[i].grid(row=(i//4)*2, column=i%4, sticky="NEWS")

            sep = ttk.Separator(top, orient='horizontal')
            sep.grid(row=1, column=0, columnspan=4, sticky="WE", pady=5, ipady=5)

            quit_button = tk.Button(top, text="Close", command=top.destroy)
            quit_button.grid(column=0, columnspan=4, row=3, sticky="WE")

            return top

        return day_weather()

    def make_extra(self, day):
        return  {'Temperature feels like': day['main']['feels_like'], 'Atmosphere Pressure': day['main']['pressure'],
                 'Air Humidity': day['main']['humidity'], 'wind': day['wind']}

    def make_day(self, day):
        current_date = datetime.datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S")
        weather_descript = day['weather'][0]['description']
        temperature = day['main']['temp']
        icon = day['weather'][0]['icon']
        extra = self.make_extra(day)
        return {'date': current_date, 'description': weather_descript, 'temp': temperature, 'icon': icon, 'extra': extra}

    def settings(self):

        def on_closing():
            if tk.messagebox.askyesno("Quit", "Do you want to quit?\nTo save your settings, you have to press OK"):
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
        API_entry.grid(row=0, column=4, sticky="NEWS", ipady=10, pady=5, columnspan=3)

        tim_lab = tk.Label(top, text="Language:")
        tim_lab.grid(row=1, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        lang_entry = tk.Entry(top, textvariable=self.lang, width=10, justify='center')
        lang_entry.grid(row=1, column=4, sticky="NEWS", ipady=5, pady=5, columnspan=3)

        tim_lab = tk.Label(top, text="City:")
        tim_lab.grid(row=2, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        city_entry = tk.Entry(top, textvariable=self.city, width=10, justify='center')
        city_entry.grid(row=2, column=4, sticky="NEWS", ipady=5, pady=5, columnspan=3)

        unit_label = tk.Label(top, text='Units:')
        unit_label.grid(row=3, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        metric_unit = tk.Radiobutton(top, text="metric", variable=self.units, value="metric")
        metric_unit.grid(row=3, column=4, sticky="NEWS", ipady=5, pady=5, padx=5)

        imperial_unit = tk.Radiobutton(top, text="imperial", variable=self.units, value="imperial")
        imperial_unit.grid(row=3, column=5, sticky="NEWS", ipady=5, pady=5, padx=5)

        kelvin_unit = tk.Radiobutton(top, text="kelvin", variable=self.units, value="kelvin")
        kelvin_unit.grid(row=3, column=6, sticky="NEWS", ipady=5, pady=5, padx=5)

        detailed_label = tk.Label(top, text='Detailed settings')
        detailed_label.grid(row=4, column=0, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        is_detailed = tk.Checkbutton(top, text="Detailed Forecast", variable=self.details, onvalue=1, offvalue=0)
        is_detailed.grid(row=4, column=4, sticky="NEWS", columnspan=4, ipady=5, pady=5, padx=5)

        B = tk.Button(top, text="OK", command=top.destroy)
        B.grid(row=5, column=0, columnspan=8, sticky="NEWS", padx=2, pady=2)

        top.wait_window()

        if (old_city != self.city.get()):
            self.find_city()

        self.grad = " °C" if (self.units.get() == "metric") else " °F" if (self.units.get() =="imperial") else " °K"
        cast = self.forecast()

        self.weather_now_update()

        for i in range(len(self.three_days_list)):
            for day in cast:
                if (str(day['dt_txt']) == str(self.three_days_list[i].date)):
                    self.check_changes(self.three_days_list[i], day)
                    break
        for i in range(len(self.five_days_list)):
            for day in cast:
                if (str(day['dt_txt']) == str(self.five_days_list[i].date)):
                    self.check_changes(self.five_days_list[i], day)
                    break

    def check_changes(self, change_day, day):
        change_day.temperature["text"] = str(day['main']['temp']) + self.grad
        change_day.descript["text"] = day['weather'][0]['description']
        if (self.details.get() != 0):
            change_day.extra_info = self.make_extra(day)
            change_day.fill_extra()
        else:
            change_day.extra_info = {}
            change_day.extra['text'] = ''
        if (change_day.icon_num != day['weather'][0]['icon']):
            change_day.icon_num = day['weather'][0]['icon'] + "@4x"
            change_day.load_icon(change_day.link + change_day.icon_num + ".png")

    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")

    def find_city(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': self.city.get(), 'type': 'like', 'units': self.units.get(), 'APPID': self.appid.get()})
            data = res.json()
            self.city_id = data['list'][0]['id']
        except Exception as e:
            #print("Exception (find):", e)
            tk.messagebox.showerror("City Error",
                                    "It seems, entered city does not exist.\n"
                                    "It has been restored to default.\nPlease, check spelling of that city!")
            self.defaults()
            self.find_city()
            pass

    def getweather(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': self.city_id, 'units': self.units.get(), 'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            data['dt_txt'] = str(datetime.datetime.now()).split('.')[0]
            return data
        except Exception as e:
            tk.messagebox.showerror("Settings Error",
                                    "It seems, your settings are incorrect.\n"
                                    "It has been restored to defaults.\nPlease, check them!")
            self.defaults()
            return self.getweather()
            pass

    def forecast(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'id': self.city_id, 'units': self.units.get(), 'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            return data['list']
        except Exception as e:
            #print("Exception (forecast):", e)
            tk.messagebox.showerror("API Error",
                                    "It seems, that your API is incorrect.\n"
                                    "It has been restored to defaults.\nPlease, check your API!")
            self.defaults()
            return self.forecast()
