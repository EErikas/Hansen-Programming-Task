# Programming task 
This is my submission for the programming task described below. The script has been implemented using Python programming language and has been tested on machines running `Windows 11` and `Ubuntu 20.04` with `Python 3.10.10`.

## Running the Script
To run the script, navigate to the project root and enter the following command in the terminal:
```
python main.py <pattern> <integers>
```
For example:
```
python main.py TST 3 8 5
```
In this case, you would see the following output:
```
Tough, Soft and Tough.
Tough, Soft, Tough, Tough, Soft, Tough, Tough and Soft.
Tough, Soft, Tough, Tough and Soft.
```
You can also ask for a hint if you need a reminder of what positional arguments are needed by calling 
```
python main.py -h
```

Once the script is launched, a log file called `main.log` is created in the project root, which stores errors that might occur during the launch of the script.

## Running the Tests
The unit tests for the functions have been implemented using the built-in Python `unittest` module. 
To run the tests, navigate to the root directory and enter the following command:
```
python -m unittest discover
```

## Thoughts on the assignment
The completion of this task took around 4 hours. 

Overall, I enjoyed the challenge. The most difficult part was thinking of interesting edge cases that might come up in the solution. This is especially true when it comes to functions like `validate_ints()` where the original idea was to only check if the provided value can be converted to an integer but later it was decided to add checks if the integer is greater than 0, as the integers should represent the length of the output. 
Once the aforementioned edge cases and regular test cases were conceptualized it took some time to write and organize the unit tests, especially for functions that required the creation of mock logging and standard output.
