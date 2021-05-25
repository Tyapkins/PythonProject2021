"""Weather visualization."""
import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk


class weather_day(tk.Frame):
    """Visualized wetaher class."""

    def __init__(self, master=None, max_width=28, date='', icon_num='',
                 temp='', descrip='', extra={}, **kw):
        """Initialize."""
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

        self.day = tk.Label(self, justify="center",
                            text=actual_name, width=self.mwidth)
        self.day.grid(row=0, column=0, sticky="NEWS")

        self.icon = tk.Label(self, text="No Icon Yet",
                             justify="center", width=self.mwidth)
        self.icon.grid(row=1, column=0, sticky="NEWS")

        self.descript = tk.Label(self, text=self.description,
                                 justify="center", width=self.mwidth)
        self.descript.grid(row=2, column=0, sticky="NEWS")

        self.temperature = tk.Label(self, text=self.temp,
                                    justify="center", width=self.mwidth)
        self.temperature.grid(row=3, column=0, sticky="NEWS")

        self.extra = tk.Label(self, justify="center", width=self.mwidth)
        self.extra.grid(row=4, column=0, sticky="NEWS")

        if len(self.extra_info) > 0:
            self.fill_extra()

        self.link = "http://openweathermap.org/img/wn/"

        self.load_icon(self.link + self.icon_num + ".png")

    def deg_to_dir(self, angle):
        """Convert wind degrees to direction."""
        dirs = [_('↑ N'), _('↗ NNE'), _('↗ NE'), _('↗ ENE'),
                _('→ E'), _('↘ ESE'), _('↘ SE'), _('↘ SSE'),
                _('↓ S'), _('↙ SSW'), _('↙ SW'), _('↙ WSW'),
                _('← W'), _('↖ WNW'), _('↖ NW'), _('↖ NNW')]
        ix = round(angle / (360. / len(dirs)))
        return dirs[ix % len(dirs)]

    def fill_extra(self):
        """Fill detailed information for weather."""
        self.extra['text'] = ''
        for info in self.extra_info:
            if (info != 'wind'):
                if self.temperature['text'][-1] == "C" or \
                        self.temperature['text'][-1] == "K":
                    measurement = "%" if (info == _("Air Humidity")) \
                        else ("°"+self.temperature['text'][-1] if
                              (info == _("Temperature feels like")) else
                              _("hPa") if (info == _("Atmosphere Pressure"))
                              else '')
                else:
                    measurement = "%" if (info == _("Air Humidity")) \
                        else ("°F" if (info == _("Temperature feels like"))
                              else _("hPa")
                              if (info == _("Atmosphere Pressure"))
                              else '')
                self.extra['text'] += "{a}: {b} {c},\n".\
                    format(a=info, b=self.extra_info[info], c=measurement)
            else:
                self.extra['text'] += "{a}: {b} {s},\n{c}: {d}".\
                    format(a=_("Wind Speed"),
                           b=self.extra_info['wind']['speed'],
                           c=_("Wind Direction"),
                           d=self.deg_to_dir(self.extra_info['wind']['deg']),
                           s=_("m/s") if
                           self.temperature['text'][-1] == "C"
                           else _("mp/h"))

    def load_icon(self, url):
        """Load weather icon from site."""
        self.icon['text'] = _('Loading picture...')
        self.update()
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            self.icon['text'] = _('Timeout error')
        else:
            if response.status_code != 200:
                self.icon['text'] =\
                    _('HTTP error ') + str(response.status_code)
            else:
                pil_image = Image.open(BytesIO(response.content))
                image = ImageTk.PhotoImage(pil_image)
                self.icon.config(image=image, text='')
                self.icon.image = image
