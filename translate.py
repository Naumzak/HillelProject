def translate_func(text, source, target):
    import requests

    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = f"q={convert_to_hex(text)}&target={target}&source={source}"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-key': "9ec145bc96msh413044f3f1dcc7cp145245jsnc371b2c18f67",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def convert_to_hex(text):
    ascii_values = ''
    for character in text:
        ascii_values += ("%" + character.encode('utf-8').hex())
    return ascii_values

