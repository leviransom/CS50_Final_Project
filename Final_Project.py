from bs4 import BeautifulSoup
import requests
import re


class Script:
    def __init__(self):
        """Constructs a script object using a specified IMSDB url"""

        self._url = self.get_url()
        self._response = self.get_response(self.url)
        self.create_script_file()
        self.iterable = self.create_iterable_script()

    def __str__(self):
        """Returns a string representation of the script"""

        return f"\nSCRIPT DATA BELOW:\n\nURL: {self.url}\nResponse: {self.response}\n"

    @property
    def url(self):
        return self._url

    @property
    def response(self):
        return self._response

    def get_url(self):
        """Prompts user for a movie name and constructs a url using the name"""

        the = "the "
        conj = (
            "an",
            "the",
            "and",
            "but",
            "or",
            "for",
            "nor",
            "in",
            "on",
            "under",
            "with",
            "to",
            "of",
            "by",
            "as",
        )
        movie = input("Insert a movie name: ").strip().title()
        words = movie.split()
        path = ""
        for index, word in enumerate(words):
            if word.lower() in conj:
                if index == 0 and word.lower() != the.strip():
                    path += f"{word} "
                else:
                    word = word.lower()
                    path += f"{word} "
            else:
                path += f"{word} "
        if path.startswith(the):
            path = path.replace(the, '').strip() + ",-The"
        
        
            

            
        path = path.strip().replace(" ", "-") + ".html"
        
        return f"https://imsdb.com/scripts/{path}"

    def get_response(self, url):
        """Uses the request library to send a GET request to the url and stores the response"""

        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(
                f"Did not receive a status code of 200, instead received: {response.status_code}"
            )

    def create_script_file(self):
        """Creates a text file containing a script scraped from an html file"""

        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.script_text = self.soup.find("pre")
        with open("new_script.txt", "w") as file:
            if self.script_text.text.strip():
                file.write(self.script_text.text)
            else:
                raise Exception(f"There is no script at {self.url}")

    def create_iterable_script(self):
        """Returns a list of seperate lines within the script"""

        iterable = self.script_text.text.splitlines()
        return iterable


class Script_Analyzer(Script):
    def __init__(self):
        """Will construct an Analyzer object and inherit the attributes from a Script object."""

        super().__init__()

    def __str__(self):
        """Returns a string representation of the analyzer object"""

        return f"Currently analyzing the script located at: {self.url}"

    def count_lines(self):
        """Returns the number of lines that a script contains"""

        line_count = 0
        for line in self.iterable:
            if line.strip() == "":
                continue
            else:
                line_count += 1
        return f"Total lines in script: {line_count}"

    def count_words(self):
        """Returns the number of spoken and nonspoken words"""

        word_list = re.findall(r"\b\w+\b", self.script_text.text)
        return f"Total spoken and nonspoken words in script: {len(word_list)}"

    def count_spec_word(self):
        """Returns the number of times a specific word is used"""

        spec_word = input("Insert a word: ").strip()
        word_list = re.findall(rf"{spec_word}", self.script_text.text, re.IGNORECASE)
        return f"{spec_word} is used {len(word_list)} times"

    def fetch_spec_word_lines(self):
        """Returns each line that a specific word is used in"""

        spec_sents = ""
        spec_word = input("Insert a word: ").strip()
        sentence_pattern = r"(?<=[.!?])\s+"
        sentences = re.split(sentence_pattern, self.script_text.text)
        for sentence in sentences:
            if re.search(re.escape(spec_word), sentence, re.IGNORECASE):
                spec_sents += f"{str(sentence.replace('*', '').replace('The Wolf of Wall Street   Buff Revised Pages   3/5/13', '').strip())}\n"
        
        return spec_sents

    def fetch_char_lines(self):
        """Returns each line associated with a specific character"""

        char_lines = []
        is_char_line = False
        char = input("Insert character name: ").strip().upper()
        for line in self.iterable:
            if line.strip().startswith(char):
                is_char_line = True
                char_lines.append(line.strip())
            elif is_char_line and line.strip():
                char_lines.append(line.strip())
            else:
                is_char_line = False
        lines = ""
        for line in char_lines:
            if str(line.endswith("*")):
                line = line.replace("*", "")    
            if re.match(r'^[0-9]+\.$', line):
                continue
            elif "Buff Revised Pages" in line:
                continue
            else:
                lines += f"{line}\n" 
        lines_list = lines.split("\n")
        
        
        if len(lines_list) > 50:
            prompt = input(f"{char.title()} has more than 50 lines. Would you like to see the first 50 or all? (answer 'first 50' or 'all'): ").strip()
            if prompt.lower().startswith("f"):
                counter = 0
                lines = ""
                for i in lines_list:
                    if counter == 50:
                        break
                    elif counter < 50:
                        lines += f"{i}\n"
                        if i.startswith(char) == False:    
                            counter += 1
                return lines
            elif prompt.lower().startswith("all"):      
                return lines
            else:
                return f"Not showing {char.title()}'s lines"
        else:
            return lines
                    
                    
            
        

    def fetch_chars(self):
        """Returns each character whose name is denoted by two words"""
        # This function requires additional testing/ manipulation as it will sometimes incorrectly provide
        # output that is not a character but fits within the criteria

        chars = set()
        pattern = r"^[A-Z].*[A-Z]$"
        outliers = ("V/0", "O.S", "EXT.", "INT.", "EX.", "END")

        for line in self.iterable:
            line = line.strip()
            if line.isupper():
                if re.match(pattern, line):
                    if not line.startswith(outliers) and not line.endswith(outliers):
                        if len(line.split()) <= 2:
                            chars.add(line)
        sorted(chars)
        output = ""
        for i in chars:
            output += f"{i}\n"
        
        return output


def main():
    url = 'https://imsdb.com/scripts/Star-Wars-A-New-Hope.html'
    test_url = "https://imsdb.com/Movie%20Scripts/Lord%20of%20the%20Rings:%20Fellowship%20of%20the%20Ring,%20The%20Script.html"
    script = Script_Analyzer()
    print(script.count_spec_word())
    print(script.fetch_spec_word_lines())
    

if __name__ == "__main__":
    main()
