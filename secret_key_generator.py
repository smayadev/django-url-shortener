import random

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
secret_key = ''.join(random.choice(chars) for i in range(50))
print(secret_key)