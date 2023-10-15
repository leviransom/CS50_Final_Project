from bs4 import BeautifulSoup
import requests
import re



class Script():
    


    def __init__(self, url):

        '''Constructs a script object using a specified IMSDB url'''

        self.url = self.get_url()
        self.response = self.get_response(self.url)
        self.create_script_file()
        self.iterable = self.create_iterable_script()

    def __str__(self):

        '''Returns a string representation of the script'''

        return f'\nSCRIPT DATA BELOW:\n\nURL: {self.url}\nResponse: {self.response}\n'
    
    def get_url(self):

        '''Prompts user for a movie name and constructs a url using the name'''

        the = 'the '
        conj = ["an", "the", "and", "but", "or", "for", "nor", "in", "on", "under", "with", "to", "of", "by", "as"]
        movie = input("Insert a movie name: ").strip().title()
        words = movie.split()
        path = ""
        for word in words:
            if word.lower() in conj:
                word = word.lower()
                path += f"{word} "
            else:
                path += f"{word} "
        if path.lower().startswith(the):
            path = path.replace(the, '').strip() + ",-The"
        path = path.strip().replace(" ", "-") + ".html"
        return f"https://imsdb.com/scripts/{path}"
    
    def get_response(self, url):
        
        '''Uses the request library to send a GET request to the url and stores the response'''

        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f'Did not receive a status code of 200, instead received: {response.status_code}')
                
    def create_script_file(self):

        '''Creates a text file containing a script scraped from an html file'''

        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.script_text = self.soup.find('pre')
        with open('new_script.txt', 'w') as file:
            try:
                file.write(self.script_text.text)
            except:
                raise Exception(f'There is no script at {self.url}')

    def create_iterable_script(self):

        '''Returns a list of seperate lines within the script'''

        iterable = self.script_text.text.splitlines()
        return iterable


class Script_Analyzer(Script):



    def __init__(self, url):

        '''Will construct an Analyzer object and inherit the attributes from a Script object.'''

        super().__init__(url)

    def __str__(self):

        '''Returns a string representation of the analyzer object'''

        return f'Currently analyzing the script located at: {self.url}'

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
        lines = ""
        for line in self.iterable:
            if re.search(re.escape(spec_word), line, re.IGNORECASE):
                lines += f"{line}\n"
        return lines
    def fetch_char_lines(self):
        
        with open('new_script.txt', 'r') as file:
            script_lines = file.readlines()

            char_lines = []
            is_char_line = False
            char = input("Insert Character: ").strip().upper()
            for line in script_lines:
                if line.strip().startswith(char):
                    is_char_line = True
                    char_lines.append(line.strip())
                elif is_char_line and line.strip():
                
                    char_lines.append(line.strip())
                else:
                    is_char_line = False
                
            lines = ""
            for line in char_lines:
                lines += f"{line}\n"
                
            return lines


def main():
    url = 'https://imsdb.com/scripts/Star-Wars-A-New-Hope.html'
    test_url = "https://imsdb.com/Movie%20Scripts/Lord%20of%20the%20Rings:%20Fellowship%20of%20the%20Ring,%20The%20Script.html"
    star_wars = Script_Analyzer(url)
    print(star_wars.fetch_char_lines())
    

if __name__ == '__main__':  
    main()