import sys

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    data = sys.stdin.read().strip()
    if not data:
        sys.exit(0)
    try:
        n = int(data)
    except ValueError:
        print("Invalid input")
        sys.exit(1)
    try:
        print(factorial(n))
    except ValueError as e:
        print(e)