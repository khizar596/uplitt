import string
import random # define the random module
def string_generator():
    S = 80
    ran = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+ string.digits, k = S))
    return str(ran)

def OTP_numbr():
    number = random.randint(1000, 9999)
    return number

