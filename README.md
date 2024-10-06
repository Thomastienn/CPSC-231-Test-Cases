# Test cases for CPSC 231 assignments

>[!CAUTION]
>- I only test on windows in pycharm. There could be errors with VSCode or people using Mac. <br>
>- The test might be slow, it could take half a minute.

## What it does?
It will run many cases for you so you don't have to enter each one. As the autograde only has 5 test cases for you guys which is so little, this will provide you more several cases. Contributions of more test cases is really appreciated.

## How to use?
1. Download the dependencies
2. Choose the assignment you want.
3. Download the file into the same directory as your assignment
4. In the file, there will be the file path like this

```python
def setUp(self):
    self.file_path = "../analyse_fert_rate.py"
```
5. Change the file directory to your file (if it is in the same directory, it should be like this file_name.py)
6. If you use windows, you don't need to change anything. If you use mac, change wexpect to pexpect.
7. Run the file and see the result


## Dependencies
- if you are using windows ```pip install wexpect``` 
- if you use mac ```pip install pexpect```
