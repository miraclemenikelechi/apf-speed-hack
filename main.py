from fastapi import FastAPI, Query, HTTPException

server = FastAPI()


@server.post("/calculate")
async def calculate_two_values(num1: int, num2: int, operation: str):
    """
    A function to calculate the result of two values based on the specified operation.

    Parameters:
    - num1 (int): The first number for the operation.
    - num2 (int): The second number for the operation.
    - operation (str): The operation to perform on the two numbers. Can be one of: '+' or 'add', '-' or 'sub', '*' or 'mul', '/' or 'div'.

    Returns:
    - The result of the operation on num1 and num2, or an error message if the operation is invalid or division by zero occurs.
    """

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
                return "Error: Division by zero"
        case _:
            return "Error: Invalid operation"


@server.post("/factorial")
async def calculate_factorial_route(num: int = Query(example=5)):
    """
    An asynchronous function that handles POST requests to '/factorial' endpoint.
    It takes an integer 'num' as input and returns the factorial of 'num'.
    """

    def calculate_factorial(num: int):
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
        - principal: float, the principal amount
        - rate: float, the interest rate
        - time: int, time period in years

    Returns:
        A dictionary containing the calculated simple interest.
    """

    simple_interest = (principal * rate * time) / 100
    return {"simple_interest": simple_interest}


@server.post("/palindrome")
async def palindrome_checker(text: str = Query(example="racecar")):
    """
    A function that checks if a given text is a palindrome.

    Parameters:
    text (str): The text to be checked for palindrome.

    Returns:
    dict: A dictionary containing the result of the palindrome check.
    """

    is_palindrome = text == text[::-1]
    return {"is_palindrome": is_palindrome}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:server", host="0.0.0.0", port=8000, reload=True)