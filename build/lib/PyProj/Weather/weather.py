"""Weather Application."""
import sys
sys.path.insert(0, '..')
import tkinter as tk
from tkinter import ttk
from skeleton import Application
import requests
import datetime

from day import weather_day


class WeatherApp(Application):
    """Application for weather forecast."""

    def __init__(self, master=None, mainm=None, **kw):
        """Initialize application."""
        master.minsize(1150, 850)
        master.maxsize(1200, 900)
        super().__init__(master=master, **kw)
        self.back = mainm

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

        self.weatherButton = tk.Button(self, text=_("Weather in a moment"),
                                       command=self.weather_now_update)
        self.weatherButton.grid(row=1, column=0, sticky="NEWS", rowspan=2)

        self.weather_now()

        self.separ = ttk.Separator(self, orient='horizontal')
        self.separ.grid(row=3, column=0, columnspan=4,
                        sticky="WE", pady=5, ipady=5)

        self.weathers = ttk.Notebook(self)
        self.weathers.grid(row=4, column=0, sticky="NEWS", columnspan=2)

        self.three_days = ttk.Frame(self.weathers, width=300, height=200)
        self.five_days = ttk.Frame(self.weathers, width=300, height=200)

        self.weathers.add(self.three_days, text=_("3 days"))
        self.weathers.add(self.five_days, text=_("5 days"))

        now_date = datetime.datetime.now()
        forcst = self.forecast()

        for day in forcst:
            current_date = datetime.datetime.strptime(
                day['dt_txt'], "%Y-%m-%d %H:%M:%S")
            diff = datetime.timedelta(hours=1, minutes=30)
            diction = self.make_day(day)
            if (abs(current_date-now_date) < diff):
                self.days[0] = diction
            elif (current_date.hour == 12 and current_date
                    .day != now_date.day):
                if (diction not in self.days):
                    self.days.append(diction)

        self.three_days_list = []
        self.three_buttons = []
        self.fill_mas(self.three_days_list, self.three_buttons,
                      self.three_days, 47, 3)

        self.five_days_list = []
        self.five_buttons = []
        self.fill_mas(self.five_days_list, self.five_buttons,
                      self.five_days, 28, 5)

        self.link = "http://openweathermap.org/img/wn/"

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=_("Settings"), command=self.settings)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=_("Go to Main Menu"),
                                  command=self.go_back)
        self.filemenu.add_command(label=_("Close"), command=self.quit)
        self.menubar.add_cascade(label=_("Menu"), menu=self.filemenu)

        self.master.config(menu=self.menubar)

    def defaults(self):
        """Set defaul settings."""
        self.appid.set("d83a96348dfb13f8e92f0ae8929e1eff")
        self.city.set('Tver')
        self.units.set('metric')
        self.grad = " °C"
        self.details.set(0)
        self.lang.set('en')
        self.find_city()

    def weather_now(self):
        """Display current weather."""
        day = self.make_day(self.getweather())
        extra_info = day['extra'] if self.details.get() != 0 else {}
        self.wnow = weather_day(master=self,
                                icon_num=day['icon']+"@4x",
                                temp=str(day['temp'])+self.grad,
                                date=day['date'], descrip=day['description'],
                                extra=extra_info)
        self.wnow.grid(row=1, column=1, rowspan=2)

    def weather_now_update(self):
        """Update current weather."""
        self.check_changes(self.wnow, self.getweather())

    def fill_mas(self, mas, buttons, tab, section_width, max_size):
        """Fill weather list with information."""
        for i in range(max_size):
            new_day = self.days[i]
            mas.append('')
            extra_info = new_day['extra'] if self.details.get() != 0 else {}
            mas[i] = weather_day(master=tab, max_width=section_width,
                                 icon_num=new_day['icon']+"@4x",
                                 temp=str(new_day['temp'])+self.grad,
                                 date=new_day['date'],
                                 descrip=new_day['description'],
                                 extra=extra_info)
            mas[i].grid(row=0, column=i, sticky="NEWS")

            buttons.append('')
            buttons[i] = tk.Button(master=tab,
                                   command=(lambda x=new_day['date'].day:
                                            self.more(x)),
                                   text=_("More Information"))
            buttons[i].grid(row=1, column=i, sticky="NEWS")

    def more(self, day_num):
        """Generate function to display weather day."""
        def day_weather():
            """Organize detailed weather window for a specific day."""
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

            for i in range(len(final_mas)):
                new_day = final_mas[i]
                mas_days.append('')
                extra_info = final_mas[i]['extra'] if \
                    self.details.get() != 0 else {}
                mas_days[i] = weather_day(top,
                                          icon_num=new_day['icon']+"@2x",
                                          temp=str(new_day['temp'])+self.grad,
                                          date=new_day['date'],
                                          descrip=new_day['description'],
                                          extra=extra_info,
                                          max_width=40)
                mas_days[i].grid(row=(i//4)*2, column=i % 4, sticky="NEWS")

            sep = ttk.Separator(top, orient='horizontal')
            sep.grid(row=1, column=0, columnspan=4,
                     sticky="WE", pady=5, ipady=5)

            quit_button = tk.Button(top, text=_("Close"), command=top.destroy)
            quit_button.grid(column=0, columnspan=4, row=3, sticky="WE")

            return top

        return day_weather()

    def make_extra(self, day):
        """Use some details for weather forecst."""
        return {_('Temperature feels like'): day['main']['feels_like'],
                _('Atmosphere Pressure'): day['main']['pressure'],
                _('Air Humidity'): day['main']['humidity'],
                'wind': day['wind']}

    def make_day(self, day):
        """Transform Forecast info to information, that easy to process."""
        current_date = datetime.datetime.strptime(day['dt_txt'],
                                                  "%Y-%m-%d %H:%M:%S")
        weather_descript = day['weather'][0]['description']
        temperature = day['main']['temp']
        icon = day['weather'][0]['icon']
        extra = self.make_extra(day)
        return {'date': current_date, 'description': weather_descript,
                'temp': temperature, 'icon': icon, 'extra': extra}

    def settings(self):
        """Make settings window."""
        def on_closing():
            """Do something when window is closed."""
            if tk.messagebox.askyesno(_("Quit"),
                                      _("Do you want to quit?\n"
                                        "To save your settings,"
                                        "you have to press OK")):
                top.destroy()

        top = tk.Toplevel(self)
        top.resizable(False, False)
        top.protocol("WM_DELETE_WINDOW", on_closing)
        top.focus_set()
        top.grab_set()

        old_city = self.city.get()

        tim_lab = tk.Label(top, text="API:")
        tim_lab.grid(row=0, column=0, sticky="NEWS",
                     columnspan=4, ipady=10, pady=5, padx=5)

        API_entry = tk.Entry(top, textvariable=self.appid,
                             width=35, justify='center')
        API_entry.grid(row=0, column=4, sticky="NEWS",
                       ipady=10, pady=5, columnspan=3)

        tim_lab = tk.Label(top, text=_("Language:"))
        tim_lab.grid(row=1, column=0, sticky="NEWS",
                     columnspan=4, ipady=5, pady=5, padx=5)

        lang_entry = tk.Entry(top, textvariable=self.lang,
                              width=10, justify='center')
        lang_entry.grid(row=1, column=4, sticky="NEWS",
                        ipady=5, pady=5, columnspan=3)

        tim_lab = tk.Label(top, text=_("City:"))
        tim_lab.grid(row=2, column=0, sticky="NEWS",
                     columnspan=4, ipady=5, pady=5, padx=5)

        city_entry = tk.Entry(top, textvariable=self.city,
                              width=10, justify='center')
        city_entry.grid(row=2, column=4, sticky="NEWS",
                        ipady=5, pady=5, columnspan=3)

        unit_label = tk.Label(top, text=_('Units:'))
        unit_label.grid(row=3, column=0, sticky="NEWS",
                        columnspan=4, ipady=5, pady=5, padx=5)

        metric_unit = tk.Radiobutton(top, text=_("metric"),
                                     variable=self.units, value="metric")
        metric_unit.grid(row=3, column=4, sticky="NEWS",
                         ipady=5, pady=5, padx=5)

        imperial_unit = tk.Radiobutton(top, text=_("imperial"),
                                       variable=self.units, value="imperial")
        imperial_unit.grid(row=3, column=5, sticky="NEWS",
                           ipady=5, pady=5, padx=5)

        kelvin_unit = tk.Radiobutton(top, text=_("kelvin"),
                                     variable=self.units, value="kelvin")
        kelvin_unit.grid(row=3, column=6, sticky="NEWS",
                         ipady=5, pady=5, padx=5)

        detailed_label = tk.Label(top, text=_('Detailed settings'))
        detailed_label.grid(row=4, column=0, sticky="NEWS",
                            columnspan=4, ipady=5, pady=5, padx=5)

        is_detailed = tk.Checkbutton(top, text=_("Detailed Forecast"),
                                     variable=self.details,
                                     onvalue=1, offvalue=0)
        is_detailed.grid(row=4, column=4, sticky="NEWS",
                         columnspan=4, ipady=5, pady=5, padx=5)

        B = tk.Button(top, text="OK", command=top.destroy)
        B.grid(row=5, column=0, columnspan=8,
               sticky="NEWS", padx=2, pady=2)

        top.wait_window()

        if (old_city != self.city.get()):
            self.find_city()

        self.grad = " °C" if (self.units.get() == "metric") \
            else " °F" if (self.units.get() == "imperial") else " °K"
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
        """Check if forecast changed for some reason."""
        change_day.temperature["text"] = str(day['main']['temp']) + self.grad
        change_day.descript["text"] = day['weather'][0]['description']
        if (self.details.get() != 0):
            change_day.extra_info = self.make_extra(day)
            change_day.fill_extra()
        else:
            change_day.extra_info = {}
            change_day.extra['text'] = ''
        if (change_day.icon_num != day['weather'][0]['icon']):
            change_day.\
                icon_num = day['weather'][0]['icon'] + "@4x"
            change_day.load_icon(
                change_day.link + change_day.icon_num + ".png")

    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")

    def find_city(self):
        """Find city id by its name."""
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': self.city.get(), 'type': 'like',
                                       'units': self.units.get(),
                                       'APPID': self.appid.get()})
            data = res.json()
            self.city_id = data['list'][0]['id']
        except Exception:
            tk.messagebox.showerror(_("City Error"),
                                    _("It seems, "
                                      "entered city does not exist.\n"
                                    "It has been restored to default.\n"
                                      "Please, check spelling of that city!"))
            self.defaults()
            self.find_city()
            pass

    def getweather(self):
        """Get current weather from the site."""
        try:
            res = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={'id': self.city_id, 'units': self.units.get(),
                        'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            data['dt_txt'] = str(datetime.datetime.now()).split('.')[0]
            return data
        except Exception:
            tk.messagebox.showerror(_("Settings Error"),
                                    _("It seems, your settings"
                                      "are incorrect.\n"
                                    "It has been restored to defaults.\n"
                                      "Please, check them!"))
            self.defaults()
            return self.getweather()
            pass

    def forecast(self):
        """Get weather forecast from site."""
        try:
            res = requests.get(
                "http://api.openweathermap.org/data/2.5/forecast",
                params={'id': self.city_id, 'units': self.units.get(),
                        'lang': self.lang.get(), 'APPID': self.appid.get()})
            data = res.json()
            return data['list']
        except Exception:
            tk.messagebox.showerror(_("API Error"),
                                    _("It seems, that your API is incorrect.\n"
                                    "It has been restored to defaults.\n"
                                      "Please, check your API!"))
            self.defaults()
            return self.forecast()
