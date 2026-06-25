BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def encode(num):
    if num == 0:
        return BASE62[0]

    result = ""

    while num > 0:
        remainder = num % 62
        result = BASE62[remainder] + result
        num //= 62

    return result