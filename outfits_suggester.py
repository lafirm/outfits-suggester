# import required libraries
from tkinter import *  # importing all modules from tkinter package
# when we use "import tkinter as tk", we have to add "tk" at the front of all widget names
from tkinter.ttk import Combobox  # combo box is defined in the ttk module of tkinter package
import requests  # importing requests library for using API
from PIL import ImageTk, Image  # to insert image in our app window / frame
from tkinter import messagebox  # importing messagebox from tkinter to handle exceptions and display error messages

# initial steps - creation of window object, frame and canvas
window = Tk()  # creating app (window) object using Tk() func (some dev use the word "root"/"master" for window obj)
window.title("Outfits Suggester")  # set title for the application
window.geometry("500x700+10+10")  # set size (geometry) for the application window

frame = Frame(window, width=400, height=650)
# frame is like a container to hold widgets,
# it's similar to the window object we created earlier,
# but we can have only one window object, whereas we can have more than one frame in our app
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)  # relative position for x & y axes, center aligned

# creation of canvas
canvas = Canvas(frame, width=240, height=240)  # add "bg" parameter to visualize canvas for easy positioning
canvas.place(relx=0.2, rely=0.65)  # this position is finalised after creating all widgets (based on trial and error)


class MyWindow:
    def __init__(self, win):  # a constructor which takes window application object as an argument
        # we passed an argument called "win", which refers to either "window" object or "frame" for widget reference

        # label for welcome message and instruction
        self.lbl1 = Label(win, text="Welcome to the Outfits Suggester", font="none 14 bold")
        self.lbl1.place(x=50, y=2)  # pack() and grid() can also be used instead of place()
        self.lbl2 = Label(win, text="Please enter the following, so we can suggest the best outfit for you.")
        self.lbl2.place(x=20, y=30)

        # label and text field for full name
        self.lbl3 = Label(win, text="Full Name")
        self.lbl3.place(x=50, y=60)
        self.t1 = Entry(win)
        self.t1.place(x=200, y=60)

        # label and radio buttons for gender
        self.lbl4 = Label(win, text="Gender")
        self.lbl4.place(x=50, y=90)
        self.gender = IntVar()
        self.gender.set(1)
        self.rb1 = Radiobutton(win, text="Male", variable=self.gender, value=1)
        self.rb1.place(x=200, y=90)
        self.rb2 = Radiobutton(win, text="Female", variable=self.gender, value=0)
        self.rb2.place(x=280, y=90)

        # label and text field for age
        self.lbl5 = Label(win, text="Age")
        self.lbl5.place(x=50, y=120)
        self.t2 = Entry(win)
        self.t2.place(x=200, y=120)

        # label and text field for city
        self.lbl6 = Label(win, text="City")
        self.lbl6.place(x=50, y=150)
        self.t3 = Entry(win)
        self.t3.place(x=200, y=150)
        self.b1 = Button(win, text='Fetch', command=self.fetch)  # when fetch button is pressed, it calls fetch() func.
        self.b1.place(x=350, y=150)

        # label and text field for state
        self.lbl7 = Label(win, text="State")
        self.lbl7.place(x=50, y=180)
        self.t4 = Entry(win)
        self.t4.place(x=200, y=180)

        # label and text field for country
        self.lbl8 = Label(win, text="Country")
        self.lbl8.place(x=50, y=210)
        self.t5 = Entry(win)
        self.t5.place(x=200, y=210)

        # label and text field for temperature
        self.lbl9 = Label(win, text="Current - Temperature(C)")
        self.lbl9.place(x=50, y=240)
        self.t6 = Entry(win)
        self.t6.place(x=200, y=240)

        # label and combo box for weather condition
        self.lbl10 = Label(win, text="Current - Weather Cond.")
        self.lbl10.place(x=50, y=270)
        weather_data = ("Sunshine", "Cloudy", "Partly Cloudy", "Raining", "Snowy", "Foggy",
                        "Thunder & Lightning", "Windy")
        self.combo1 = Combobox(win, values=weather_data, state="readonly")
        self.combo1.place(x=200, y=270)

        # label and combo box for dress code
        self.lbl11 = Label(win, text="Dress Code")
        self.lbl11.place(x=50, y=300)
        dress_code_list = ("Casual", "Business Casual", "Smart Casual", "Business/Informal", "Semi-Formal",
                           "Formal/Black Tie")
        self.combo2 = Combobox(win, values=dress_code_list, state="readonly")
        self.combo2.place(x=200, y=300)
        self.dress_code = str(self.combo2.get())  # to get the content of combo2 and convert it into string format

        # reset button
        self.b2 = Button(win, text='Reset', command=self.reset)  # when reset button is pressed, it calls reset() func.
        self.b2.place(x=80, y=340)

        # submit button
        self.b3 = Button(win, text='Submit', command=self.display_clothes)
        # when submit button is pressed, it calls display_clothes() func.
        self.b3.place(x=250, y=340)

        # label to display message, once submit button is pressed
        self.lbl12 = Label(win, text="Thanks for choosing us!", font="none 10 italic", wraplength=300, justify="left")

        # initializing image variable to use in the "display()" function
        self.img = None

    def fetch(self):
        """
        It uses weather API from rapid API to fetch the values of
        country, state, temperature and weather condition value based on city name entered in the text field.
        """
        # to clear the Entry widget to be filled after "fetch" button is pressed
        self.t4.delete(0, "end")
        self.t5.delete(0, "end")
        self.t6.delete(0, "end")
        self.combo1.set(" ")
        # using rapid API to fetch country, state, temperature and weather cond. value based on city name
        # -- start of the code copied from API
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        location = str(self.t3.get())  # assigning city value entered in t3 field to 'location' variable (modified line)
        querystring = {"q": location}

        headers = {
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
            "X-RapidAPI-Key": "f686a67b07mshb0a429c52c9a635p1d1aa8jsnb4b44c442673"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        # -- end of the code copied from API
        data = response.json()  # extracting data in json format

        # extracting state, country, temp. and weather cond. of the first matching location
        state = data['location']['region']  # these key values were gathered after visualising the API result
        country = data['location']['country']
        temp_c = data["current"]["temp_c"]
        weather = data["current"]["condition"]["text"]
        # inserting state, country, temp. and weather cond. value into the respective text fields
        self.t4.insert(0, str(state))
        self.t5.insert(0, str(country))
        self.t6.insert(0, str(temp_c))
        self.combo1.set(str(weather))

        return country  # for the purpose of unit test

    def reset(self):
        """
        It resets the value entered and chosen in text fields (t1, t2, t3, t4, t5, t6), radio buttons,
        combo box (combo1 ans combo2), display messages (lbl12) and display image.
        """
        self.t1.delete(0, "end")
        self.t2.delete(0, "end")
        self.t3.delete(0, "end")
        self.t4.delete(0, "end")
        self.t5.delete(0, "end")
        self.t6.delete(0, "end")
        self.gender.set(1)  # to reset radio button
        self.combo1.set(" ")
        self.combo2.set(" ")
        self.lbl12.place_forget()
        self.img = None

        return self.t1.get()  # for the purpose of unit test

    def display(self):
        """
        It displays the image of the clothing (outfit),
        based on the information (age, gender and dress code) entered by the user.
        And it displays a message based on the weather condition outside.
        Note: It's a secondary function, which means it will be called by another function called display_clothes().
        display_clothes() function is used to handle the exceptions in display() function.
        """
        self.lbl12.place(relx=0.23, rely=0.58)  # to display message after pressing submit button

        age = int(self.t2.get())  # to get the content of t2 (text field) and convert it into integer

        # condition to display outfit image based on age, gender and dress code
        if age <= 5:
            self.img = ImageTk.PhotoImage(Image.open("child.jpg"))
            canvas.create_image(20, 20, anchor=NW, image=self.img)

        elif (age > 5) and (age < 16):
            if self.gender.get() == 1:  # if person is male (boy)
                self.img = ImageTk.PhotoImage(Image.open("teenage_boy.jpg"))
                canvas.create_image(20, 20, anchor=NW, image=self.img)
            else:  # if person is female (girl)
                self.img = ImageTk.PhotoImage(Image.open("teenage_girl.jpg"))
                canvas.create_image(20, 20, anchor=NW, image=self.img)

        elif age >= 16:
            if str(self.combo2.get()) == "Casual":
                if self.gender.get() == 1:  # if person is male
                    # open the image file & create an object from PhotoImage class of tkinter ImageTk
                    # created image object can be used to display images in labels, buttons, canvases, & text widgets
                    self.img = ImageTk.PhotoImage(Image.open("casual_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("casual_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

            elif str(self.combo2.get()) == "Business Casual":
                if self.gender.get() == 1:  # if person is male
                    self.img = ImageTk.PhotoImage(Image.open("business_casual_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("business_casual_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

            elif str(self.combo2.get()) == "Smart Casual":
                if self.gender.get() == 1:  # if person is male
                    self.img = ImageTk.PhotoImage(Image.open("smart_casual_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("smart_casual_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

            elif str(self.combo2.get()) == "Business/Informal":
                if self.gender.get() == 1:  # if person is male
                    self.img = ImageTk.PhotoImage(Image.open("business_informal_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("business_informal_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

            elif str(self.combo2.get()) == "Semi-Formal":
                if self.gender.get() == 1:  # if person is male
                    self.img = ImageTk.PhotoImage(Image.open("semi_formal_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("semi_formal_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)

            elif str(self.combo2.get()) == "Formal/Black Tie":
                if self.gender.get() == 1:  # if person is male
                    self.img = ImageTk.PhotoImage(Image.open("formal_black_tie_male.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
                else:  # if person is female
                    self.img = ImageTk.PhotoImage(Image.open("formal_black_tie_female.jpg"))
                    canvas.create_image(20, 20, anchor=NW, image=self.img)
        # condition to display message based on the weather condition
        if "cloudy" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "The weather outside seems Cloudy!\nExpect the unexpected.\nGrab an umbrella." \
                                 "Thank me later :)"
        elif "sun" in str(self.combo1.get()).lower() or "clear" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "It's a beautiful day outside! Sun is shining.\n" \
                                  "Put on some sunscreen and enjoy your day."
        elif "rain" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "It's Raining outside!\nMake sure you take your rain coats and umbrella.\nTake Care!"
        elif "snow" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "It's Snowing outside!\n"\
                                 "Wear hat, scarf, coat, gloves, socks and water-resistant shoes or boots. Or stay home"
        elif "fog" in str(self.combo1.get()).lower() or "mist" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "It's Foggy outside!\nSlow down and allow extra time to reach your destination."
        elif "thunder" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "I advise you to postpone your trip or activity today,\n" \
                                 "because of Thunder and lightning outside.\nGood Luck!"
        elif "wind" in str(self.combo1.get()).lower():
            self.lbl12["text"] = "It's important to prepare for high wind asap,\n" \
                                 "so you can get inside with plenty of time to spare."
        else:
            self.lbl12["text"] = "Please choose an appropriate weather condition from the dropdown,\n" \
                                 "so we can help you with some tips. Cheers!"

        return self.lbl12.cget("text")  # for the purpose of unit test

    def display_clothes(self):
        """
        It calls another function called display() function.
        And it's mainly used to handle the exceptions in display() function.
        """
        try:
            age = int(self.t2.get())
            if age < 0 or age > 120:
                raise ValueError
            elif (age >= 76) and (age <= 120):
                raise TypeError
            else:
                self.display()

        except ValueError:
            messagebox.showinfo("Age Error", "Please Enter Valid Age")
        except TypeError:
            messagebox.showinfo("Retirement Age", "Hi There!, It's time for the retirement, "
                                                  "Wear some Comfy clothes, sit back and relax! Hakuna Matata!")


my_window_object = MyWindow(frame)  # instantiating MyWindow Class, it automatically calls the constructor
# here, we used "frame" as an argument, so all the widgets will take frame as a reference

if __name__ == '__main__':  # for the purpose of unit test, to make the window to be displayed only in this main script
    window.mainloop()
# the above code enables window object to enter into event listening loop
# w/o this code (i.e mainloop() func), our app window won't be displayed
