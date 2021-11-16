import requests
from bs4 import BeautifulSoup
import urllib.parse


class Aeries:

    def __init__(self, username, password):

        self.username = username
        self.password = password

        self.login()

        if self.logged_in:
            self.get_classes()

    def login(self):

        data = {
            'portalAccountUsername': self.username,
            'portalAccountPassword': self.password
        }

        self.session = requests.Session()

        self.session.get(
            'https://pasadenausd.asp.aeries.net/student/LoginParent.aspx')

        send_creds = self.session.post(
            'https://pasadenausd.asp.aeries.net/student/LoginParent.aspx', data)

        parsed_post_cred_screen = BeautifulSoup(send_creds.text, features='html.parser')

        if parsed_post_cred_screen.find('span', 'errorMessage') is None:
            self.logged_in = True
        else:
            self.logged_in = True

    def get_site_html(self, site):
        return self.session.get(site).text

    def get_classes(self):

        gradebook_html = self.get_site_html(
            'https://pasadenausd.asp.aeries.net/student/GradebookSummary.aspx')

        parsed_gradebook_html = BeautifulSoup(gradebook_html, features='html.parser')

        classes = parsed_gradebook_html.find_all(
            'tr', id=lambda x: x and x.endswith('Item'))

        self.classes = {}

        for i in range(0, len(classes)):
            self.classes[classes[i].find(
                'a', 'link-gradebook-details').text] = {}
            current_class_dict = self.classes[classes[i].find(
                'a', 'link-gradebook-details').text]
            current_class_dict['name'] = classes[i].find(
                'a', 'link-gradebook-details').text
            current_class_dict['period'] = list(classes[i].findChildren())[6].text
            current_class_dict['percent_grade'] = classes[i].find('td', 'gcc-cell').text
            current_class_dict['letter_grade'] = list(classes[i].findChildren())[12].text
            current_class_dict['encoded_class_name'] = urllib.parse.quote(current_class_dict['name'])
        print(self.classes)
        return self.classes
