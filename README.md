# ZGallerie Selenium Automation Tests

## To configure this test suite locally follow below steps

1. Clone the repo to your local
2. Go to cmd and run pip install -r requirements.txt (there might be some dependencies which may not be part of this requirement.txt).
3. If there are some other dependencies, you will get an error while running this test. Install those as you see the error.


## To run all tests

**python app.py --browser <chrome/firefox/edge>**

## To run specific tests 
Identify the test file that your test resides in the folder named `tests`
**python app.py --tc test_01 --browser <chrome/firefox/edge>**
Code will look for file with name *test_01* recursively and run it 

## To run test in different modes 
python app.py --mode <iphone7/iphone8/iphonex/pixel> --tc test_01

## To run in virutal environment 
<python3> -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirement.txt
python app.py --browser <chrome/firefox/edge>
deactivate
