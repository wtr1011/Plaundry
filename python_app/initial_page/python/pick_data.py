import json

def picker():
    jsopen = open('./static/inst_data/rasp.json', 'r')
    jsload = json.load(jsopen)
    instdata = [
        jsload['washInfo']['userID'],
        jsload['washInfo']['time'],
        jsload['washInfo']['height'],
        jsload['washInfo']['weight']
        ]

    return instdata

if __name__ == "__main__":
    picker()