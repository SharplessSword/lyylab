def beautify_number(number):
    if number > 10000 or number<0.0001:
        number = format(number, '0.3e')
    elif 10000 >= number > 10:
        number = format(number, '0.1f')
    else:
        number = format(number, '0.3f')
    print(number)
beautify_number(1234)
beautify_number(1234.45678)
beautify_number(0.123456789)