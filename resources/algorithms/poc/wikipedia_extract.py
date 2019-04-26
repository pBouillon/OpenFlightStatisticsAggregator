import re
import requests

from http import HTTPStatus


API = 'https://en.wikipedia.org/w/api.php'
LOOK_FOR = 'Toronto'
# add selection escape on other symbols than `\d` or `,`
POPULATION_REGEX = r'.*?(?:population).*?(\d+(?:,\d+)+).*?'


def main():
    target = f'{API}?action=parse&page={LOOK_FOR}&format=json'
    r = requests.get(target)

    if r.status_code != HTTPStatus.OK:
        exit('Can\'t reach the API')

    data = r.json()['parse']['text']['*']
    print(re.findall(POPULATION_REGEX, data))


if __name__ == '__main__':
    main()
