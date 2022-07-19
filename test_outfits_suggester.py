# outline for this python unit test file is automatically generated with the below steps
# right-click the Class name --> select "Goto" option --> select "Test" option --> select "Create New Test"
from unittest import TestCase
from outfits_suggester import MyWindow  # added this line to use in assertEqual() function


class TestMyWindow(TestCase):
    # all the "self" parameters in the original class "MyWindow" were replaced by the "obj" object created
    def test_fetch(self, win=None):
        obj = MyWindow(win)  # instantiating MyWindow class to use the variables defined inside the class
        location = "Chennai"  # name of the city --> input
        obj.t3.insert(0, str(location))  # inserting the name of the city to the text field (t3)
        actual = MyWindow.fetch(obj)  # fetch() function returns the country name based on the city name
        expected = "India"  # this is the expected outcome for our input "Chennai"
        self.assertEqual(actual, expected)

    def test_reset(self, win=None):
        obj = MyWindow(win)  # instantiating MyWindow class to use the variables defined inside the class
        actual = MyWindow.reset(obj)
        # reset() function clears all the entries and returns the text field (t1) value for the purpose of testing
        expected = ""
        self.assertEqual(actual, expected)

    def test_display(self, win=None):
        obj = MyWindow(win)  # instantiating MyWindow class to use the variables defined inside the class
        obj.combo1.set(str("Sunshine"))  # set the value of weather condition as "Sunshine"
        age = 24
        obj.t2.insert(0, int(age))  # set the age value in "t2", otherwise it throws error due to exception handling
        actual = MyWindow.display(obj)
        #  display function displays images & messages, & returns the combo box (combo1) value for the testing purpose
        expected = "It's a beautiful day outside! Sun is shining.\n" \
                   "Put on some sunscreen and enjoy your day."
        self.assertEqual(actual, expected)
