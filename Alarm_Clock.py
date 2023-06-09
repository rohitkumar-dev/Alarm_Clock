import datetime
import tkinter as tk
from tkinter import messagebox

class AlarmClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Alarm Clock')
        self.geometry('400x300')
        self.current_alarm = None
        self.clock_format = tk.StringVar(value='12')
        self.am_pm = tk.StringVar(value='AM')

        self.label = tk.Label(self, text='Set Alarm Time:')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.format_label = tk.Label(self, text='Clock Format:')
        self.format_label.pack()

        self.format_radiobuttons = tk.Frame(self)
        self.format_radiobuttons.pack()

        self.format_12_radio = tk.Radiobutton(
            self.format_radiobuttons,
            text='12-Hour',
            variable=self.clock_format,
            value='12',
            command=self.update_clock
        )
        self.format_12_radio.pack(side=tk.LEFT)

        self.format_24_radio = tk.Radiobutton(
            self.format_radiobuttons,
            text='24-Hour',
            variable=self.clock_format,
            value='24',
            command=self.update_clock
        )
        self.format_24_radio.pack(side=tk.LEFT)

        self.am_pm_label = tk.Label(self, text='AM/PM:')
        self.am_pm_label.pack()

        self.am_pm_radiobuttons = tk.Frame(self)
        self.am_pm_radiobuttons.pack()

        self.am_radio = tk.Radiobutton(
            self.am_pm_radiobuttons,
            text='AM',
            variable=self.am_pm,
            value='AM',
            command=self.update_clock
        )
        self.am_radio.pack(side=tk.LEFT)

        self.pm_radio = tk.Radiobutton(
            self.am_pm_radiobuttons,
            text='PM',
            variable=self.am_pm,
            value='PM',
            command=self.update_clock
        )
        self.pm_radio.pack(side=tk.LEFT)

        self.current_time_label = tk.Label(self, text=self.get_current_time(), font=('Helvetica', 30))
        self.current_time_label.pack(pady=20)

        self.set_button = tk.Button(self, text='Set Alarm', command=self.set_alarm)
        self.set_button.pack()

        self.snooze_button = tk.Button(self, text='Snooze', command=self.snooze_alarm, state=tk.DISABLED)
        self.snooze_button.pack()

        self.reset_button = tk.Button(self, text='Reset', command=self.reset_alarm, state=tk.DISABLED)
        self.reset_button.pack()

        self.current_alarm_label = tk.Label(self, text='No active alarm')
        self.current_alarm_label.pack()

        self.update_clock()  # Initialize clock format

        self.update_time()  # Start updating current time

    def update_clock(self):
        format_24_selected = self.clock_format.get() == '24'
        self.format_12_radio.configure(state=tk.NORMAL if format_24_selected else tk.DISABLED)
        self.format_24_radio.configure(state=tk.NORMAL if not format_24_selected else tk.DISABLED)
        self.current_time_label.configure(text=self.get_current_time())

    def update_time(self):
        self.current_time_label.configure(text=self.get_current_time())
        self.after(1000, self.update_time)

    def get_current_time(self):
        now = datetime.datetime.now()
        if self.clock_format.get() == '12':
            return now.strftime('%I:%M:%S %p')
        else:
            return now.strftime('%H:%M:%S')

    def set_alarm(self):
        alarm_time = self.entry.get()

        try:
            alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
            if self.clock_format.get() == '12':
                if self.am_pm.get() == 'PM' and alarm_hour < 12:
                    alarm_hour += 12
                elif self.am_pm.get() == 'AM' and alarm_hour == 12:
                    alarm_hour = 0
            now = datetime.datetime.now()
            alarm = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

            if alarm < now:
                alarm += datetime.timedelta(days=1)  # Set the alarm for the next day if it's already passed

            time_difference = alarm - now
            seconds_until_alarm = time_difference.total_seconds()

            messagebox.showinfo('Alarm Set', f'Alarm set for {alarm_time}')

            self.current_alarm = self.after(int(seconds_until_alarm * 1000), self.ring_alarm)
            self.set_button.configure(state=tk.DISABLED)
            self.snooze_button.configure(state=tk.NORMAL)
            self.reset_button.configure(state=tk.NORMAL)
            self.current_alarm_label.configure(text=f'Active alarm: {alarm_time}')
        except ValueError:
            messagebox.showerror('Invalid Input', 'Please enter a valid time in HH:MM format')

    def ring_alarm(self):
        messagebox.showinfo('Alarm', 'Wake up!')
        self.snooze_button.configure(state=tk.NORMAL)

    def snooze_alarm(self):
        self.after_cancel(self.current_alarm)
        snooze_time = datetime.timedelta(minutes=5)  # Snooze for 5 minutes
        snooze_alarm = datetime.datetime.now() + snooze_time
        self.current_alarm = self.after(int(snooze_time.total_seconds() * 1000), self.ring_alarm)
        self.snooze_button.configure(state=tk.DISABLED)

    def reset_alarm(self):
        self.after_cancel(self.current_alarm)
        self.set_button.configure(state=tk.NORMAL)
        self.snooze_button.configure(state=tk.DISABLED)
        self.reset_button.configure(state=tk.DISABLED)
        self.current_alarm_label.configure(text='No active alarm')

if __name__ == '__main__':
    alarm_clock = AlarmClock()
    alarm_clock.mainloop()
