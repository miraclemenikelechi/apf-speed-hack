from fastapi import FastAPI, Query, HTTPException
from enum import Enum
from pydantic import BaseModel, Field

server = FastAPI()


class Operators(str, Enum):
    add = "+"
    sub = "-"
    mul = "*"
    div = "/"


class Calculator(BaseModel):
    num1: float = Field(description="The first number for the operation.")

    num2: float = Field(description="The first number for the operation.")

    operation: Operators = Field(
        description="The first number for the operation.", max_length=3
    )


@server.post("/calculate")
async def calculate_two_values(calculator: Calculator):
    """
    A function to calculate the result of two values based on the specified operation.

    Parameters:
    - `num1 (int)`: The first number for the operation.
    - `num2 (int)`: The second number for the operation.
    - `operation (str)`: The operation to perform on the two numbers. Can be one of: `+` or `add`, `-` or `sub`, `*` or `mul`, `/` or `div`.

    Returns:
    - The `result` of the operation on num1 and num2, or an error message if the operation is invalid or division by zero occurs.
    """

    num1 = calculator.num1
    num2 = calculator.num2
    operation = calculator.operation

    match operation:
        case "+" | "add":
            return {"result": num1 + num2}

        case "-" | "sub":
            return {"result": num1 - num2}

        case "*" | "mul":
            return {"result": num1 * num2}

        case "/" | "div":
            if num2 != 0:
                return {"result": num1 / num2}
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Division by zero",
                )

        case _:
            raise HTTPException(
                status_code=400,
                detail="Invalid operation",
            )


class TemperatureUnit(str, Enum):
    Celsius = "Celsius"
    Fahrenheit = "Fahrenheit"
    Kelvin = "Kelvin"


@server.get("/temperature")
async def convert_temperature(
    from_unit: TemperatureUnit = Query(
        description="Unit to convert from: Celsius|Fahrenheit|Kelvin"
    ),
    to_unit: TemperatureUnit = Query(
        description="Unit to convert to: Celsius|Fahrenheit|Kelvin"
    ),
    value: float = Query(description="Value to convert"),
):
    """
    Convert temperature from one unit to another.

    Args:
    - `from_unit (str)`: Unit to convert from. Should be one of 'Celsius', 'Fahrenheit', or 'Kelvin'.
    - `to_unit (str)`: Unit to convert to. Should be one of 'Celsius', 'Fahrenheit', or 'Kelvin'.
    - `value (float)`: Value to convert.

    Returns:
    - `dict`: A dictionary containing the converted value.

    Raises:
    - `ValueError`: If the input units are not valid or the conversion cannot be performed.
    - `TypeError`: If the input value is not a float.
    - `Exception`: For any other unexpected errors.
    """

    def temperature_converter(value: float, from_unit: str, to_unit: str) -> float:
        match from_unit.title():
            case "Celsius":
                match to_unit.title():
                    case "Fahrenheit":
                        return (value * 9 / 5) + 32
                    case "Kelvin":
                        return value + 273.15
                    case _:
                        return value

            case "Fahrenheit":
                match to_unit.title():
                    case "Celsius":
                        return (value - 32) * 5 / 9
                    case "Kelvin":
                        return (value - 32) * 5 / 9 + 273.15
                    case _:
                        return value

            case "Kelvin":
                match to_unit.title():
                    case "Celsius":
                        return value - 273.15
                    case "Fahrenheit":
                        return (value - 273.15) * 9 / 5 + 32
                    case _:
                        return value

    data = temperature_converter(value, from_unit, to_unit)
    return {"converted_value": data}


@server.post("/factorial")
async def calculate_factorial_route(num: int = Query(examples=5, gt=0, lt=20)):
    """
    Calculate the factorial of a given number.

    Args:
    - `num (int)`: The number for which factorial is to be calculated.

    Returns:
    - `dict`: A dictionary containing the result of the factorial calculation.

    Raises:
    - `HTTPException 400`: If the input number is negative or greater than 20.
    """

    def calculate_factorial(num: int):
        """
        Calculate the factorial of a given number recursively.

        Args:
        - `num (int)`: The number for which factorial is to be calculated.

        Returns:
        - `int`: The factorial of the input number.

        Raises:
        - `HTTPException 400`: If the input number is negative.
        """

        if num < 0:
            return "Error: Factorial of negative number not defined"
        elif num > 20:
            raise HTTPException(status_code=400, detail="Number too large")
        elif num == 0:
            return 1
        else:
            return num * calculate_factorial(num - 1)

    return {"result": calculate_factorial(num)}


@server.get("/interest")
async def calculate_interest(
    principal: float = Query(
        description="The principal amount",
    ),
    rate: float = Query(
        description="The interest rate",
    ),
    time: int = Query(
        description="Time period in years",
    ),
):
    """
    A function to calculate simple interest based on principal amount, interest rate, and time period.

    Parameters:
    - `principal (float)`: the principal amount
    - `rate (float)`: the interest rate
    - `time (int)`: time period in years

    Returns:
    - `dict`: A dictionary containing the calculated simple interest.
    """

    simple_interest = (principal * rate * time) / 100
    return {"simple_interest": simple_interest}


@server.post("/palindrome")
async def palindrome_checker(text: str = Query(examples=["racecar"])):
    """
    A function that checks if a given text is a palindrome.

    Parameters:
    - `text (str)`: The text to be checked for palindrome.

    Returns:
    - `dict`: A dictionary containing the result of the palindrome check.
    """

    is_palindrome = text == text[::-1]
    return {"word": text, "is_palindrome": is_palindrome}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:server", host="0.0.0.0", port=8000, reload=True)
