# Gmail Notifications
![image](https://user-images.githubusercontent.com/36492651/44306373-08f5ea00-a3a7-11e8-9347-8a84bcb4efab.png)

I use [Polybar](https://github.com/jaagr/polybar) and use this repo as module to it for getting notified about my gmail.

## Installation

```
git clone https://github.com/SyfiMalik/gmail-notifications.git ~/.config/polybar/ 
mv ~/.config/polybar/gmail-notifications ~/.config/polybar/gmail
cd ~/.config/polybar/gmail
./run.py
```

You'll be prompted to login to your gmail, login there, allow gmail4polybar and you'll be given a code to enter in the terminal. Enter the code and you're good to go. Now follow below steps to recieve gmail notifications in the tray.

Add these lines to your polybar main config.

```ini
[module/gmail]
type = custom/script
exec = ~/.config/polybar/gmail/launch.py
tail = true
click-left = xdg-open https://mail.google.com
```

and yeah, don't forget to enable 'gmail' module. 
