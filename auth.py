import api_auth as api_auth
from random import random, randint

uniq_key = randint (1000000000,9999999999)
api_auth.main(uniq_key)
