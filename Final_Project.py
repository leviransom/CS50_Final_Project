from bs4 import BeautifulSoup
import requests
import re



class Script():
    


    def __init__(self, url):

        '''Will construct a Script object'''

        self.url = url
        self.response = self.get_response(self.url)
        self.create_script_file()
        self.iterable = self.create_iterable_script()

    def __str__(self):

        '''Returns a string representation of the Script object'''

        return f'\nSCRIPT DATA BELOW:\n\nURL: {self.url}\nResponse: {self.response}\n'
    
    def get_response(self, url):

        '''Will retrieve a response object using the requests library and return the object if the status code is 200'''

        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Did not receive a status code of 200, instead received: {response.status_code}')
                
    def create_script_file(self):

        '''Will create a new text file and write the script scraped from the HTML onto it'''

        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.script_text = self.soup.find('pre')
        with open('new_script.txt', 'w') as file:
            file.write(self.script_text.text)

    def create_iterable_script(self):

        '''Returns a list created from the script_text variable'''

        iterable = self.script_text.text.splitlines()
        return iterable


class Script_Analyzer(Script):



    def __init__(self, url):

        '''Will construct an Analyzer object and inherit the attributes from a Script object.'''

        super().__init__(url)

    def count_lines(self):

        '''Returns the number of lines that a script contains'''

        line_count = 0
        for line in self.iterable:
            if line.strip() == '':
                continue
            else:
                line_count += 1
        return f'Total lines in script: {line_count}'
    
    def count_words(self):

        '''Returns the number of spoken and nonspoken words'''

        word_list = re.findall(r'\b\w+\b', self.script_text.text)
        return f'Total spoken and nonspoken words in script: {len(word_list)}'
    
    def count_spec_word(self):

        '''Returns the number of times a specific word is used'''

        spec_word = input('Insert a word: ').strip()
        word_list = re.findall(fr'{spec_word}', self.script_text.text, re.IGNORECASE)
        return f'{spec_word} is used {len(word_list)} times'
    
    def fetch_spec_word_lines(self):

        '''Returns each line that a specific word is used in'''

        spec_word = input('Insert a word: ').strip()
        for line in self.iterable:
            if re.search(re.escape(spec_word), line, re.IGNORECASE):
                ...






def main():
    url = 'https://imsdb.com/scripts/Star-Wars-A-New-Hope.html'
    star_wars = Script(url)
    analyzer = Script_Analyzer(url)
    print(analyzer.count_specific_word())

if __name__ == '__main__':  
    main()