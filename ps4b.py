# Problem Set 4B
# Name: Shirin Amouei
# Collaborators: None
# Time Spent: 10:00
# Late Days Used: None

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, input_text):
        '''
        Initializes a Message object

        input_text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        # Initialize attributes
        self.message_text = input_text
        
        # Get list of valid words (call load_words function)
        self.valid_words = load_words(WORDLIST_FILENAME)
             
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        
        # Getter function for accessing the text 
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        
        # Clone self.valid_words
        valid_words_copy = self.valid_words[:]
        
        # Return the copy of self.valid_words
        return valid_words_copy
        
    def make_shift_dict(self, input_shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. If 'a' is
        shifted down by 2, the result is 'c.'

        The dictionary should contain 52 keys of all the uppercase letters
        and all the lowercase letters only, mapped to their shifted values.

        input_shift: the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping letter (string) to
                 another letter (string).
        '''
        
        # Declare length of alphabet value 
        alphabet_length = len(string.ascii_letters) // 2
        
        # Create an empty dictionary to store original and mapped letters
        mapped_dictionary = {}
       
        for i in range(alphabet_length):
            index = i + input_shift
            
            # Check if shift "wraps around" the alphabet
            if index > alphabet_length -1:
                
                # Use remainder of index divided by alphabet length for mapping 
                index = index % alphabet_length 
                
            # Add lowercase & uppercase alphabet and their mapped shifted values to dictionary
            mapped_dictionary[string.ascii_lowercase[i]] = string.ascii_lowercase[index]
            mapped_dictionary[string.ascii_uppercase[i]] = string.ascii_uppercase[index]
        
        return mapped_dictionary

    def apply_shift(self, shift_dict):
        '''
        Applies the Caesar Cipher to self.message_text with letter shift
        specified in shift_dict. Creates a new string that is self.message_text,
        shifted down the alphabet by some number of characters, determined by
        the shift value that shift_dict was built with.

        shift_dict: a dictionary with 52 keys, mapping
            lowercase and uppercase letters to their new letters
            (as built by make_shift_dict)

        Returns: the message text (string) with every letter shifted using the
            input shift_dict

        '''
        
        # Create an empty string to store shifted message
        shifted_message_text = ""
        
        # Go through each character in message_text
        for i in self.get_message_text():
            
            # Check if it's an alphabet
            if i.isalpha():
                
                # Get shifted value from shift_dict
                i = shift_dict[i]
                
                # Add mapped value to final string
                shifted_message_text += i
            
            # If not an alphabet, apply no change
            else:
                shifted_message_text += i
        return shifted_message_text
        

class PlaintextMessage(Message):
    def __init__(self, input_text, input_shift):
        '''
        Initializes a PlaintextMessage object.

        input_text (string): the message's text
        input_shift: the shift associated with this message

        A PlaintextMessage object inherits from Message. It has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using the shift)
            self.encrypted_message_text (string, encrypted using self.encryption_dict)

        '''
        # Call the subclass constructor
        Message.__init__(self, input_text)
        
        # Initialize subclass attributes
        self.shift = input_shift
        self.encryption_dict = self.make_shift_dict(input_shift)
        self.encrypted_message_text = self.apply_shift(self.encryption_dict)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        
        # Getter function for accessing input_shift
        return self.shift
    
        
    def get_encryption_dict(self):
        '''
        Used to safely access a copy of self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        
        # Clone self.encryption_dict
        encryption_dict_copy = self.encryption_dict.copy()

        # Return the copy of self.valid_words
        return encryption_dict_copy
        

    def get_encrypted_message_text(self):
        '''
        Used to safely access self.encrypted_message_text outside of the class

        Returns: self.encrypted_message_text
        '''
        
        # Getter function for accessing encrypted string
        return self.encrypted_message_text

    def modify_shift(self, input_shift):
        '''
        Changes self.shift of the PlaintextMessage, and updates any other
        attributes that are determined by the shift.

        input_shift: the new shift that should be associated with this message.
        [0 <= shift < 26]

        Returns: nothing
        '''
        
        # Update shift, encryption dictionary, & encrypted message
        self.shift = input_shift
        self.encryption_dict = self.make_shift_dict(input_shift)
        self.encrypted_message_text = self.apply_shift(self.encryption_dict)
        

class EncryptedMessage(Message):
    def __init__(self, input_text):
        '''
        Initializes an EncryptedMessage object

        input_text (string): the message's text

        an EncryptedMessage object inherits from Message. It has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        # Call the subclass constructor
        Message.__init__(self, input_text)
        

    def decrypt_message(self):
        '''
        Decrypts self.message_text by trying every possible shift value and
        finding the "best" one.
        
        We will define "best" as the shift that creates the max number of
        valid English words when we use apply_shift(shift) on the message text.
        If a is the original shift value used to encrypt the message, then
        we would expect (26 - a) to be the  value found for decrypting it.

        Note: if shifts are equally good, such that they all create the
        max number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return.

        Returns: a tuple of the best shift value used to originally encrypt 
        the message (a) and the decrypted message text using that shift value
        '''
        
        # Initialize values for storing best decrypted text, best input shift, & maximum valid words in decrypted text
        best_decrypted_message_text = ""
        best_input_shift = 0
        max_valid_words = -1

        # Try 26 possible shift values
        for i in range(26):
            
            # Get shift dictionary with i 
            shift_dict = self.make_shift_dict(26 - i)
            
            # Shift/decrypt the message text with i 
            decrypted_message_text = self.apply_shift(shift_dict)
            
            # Get a list of words from shifted/decrypted message
            decrypted_message_list = decrypted_message_text.split()
            
            # Define a counter to keep track of valid words
            valid_word_counter = 0
            
            # Look for valid words in decrypted message
            for j in decrypted_message_list:
                if is_word(self.get_valid_words(), j):
                    valid_word_counter += 1
            
            # Store best results (maximum number of found valid words given a specific input shift)
            if valid_word_counter > max_valid_words:
                max_valid_words = valid_word_counter
                best_decrypted_message_text = decrypted_message_text
                best_input_shift = i
                
        return (best_input_shift, best_decrypted_message_text)
            

    
    
def test_plaintext_message():
    '''
    Write two test cases for the PlaintextMessage class here.
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what
    case(s) it is testing.
    '''

    # 1-This test is checking the setter function for modifying input_shift
    print("___Plaintext Message Test 1___")
    first_encrypted_text = PlaintextMessage("Hello!", 1)
    print("Expected Output for First Encryption: Ifmmp!")
    print("Actual Output for First Encryption:", first_encrypted_text.get_encrypted_message_text())
    first_encrypted_text.modify_shift(2) 
    print("Expected Output for Second Encryption: Jgnnq!")
    print("Actual Output for Second Encryption:", first_encrypted_text.get_encrypted_message_text())
    
    # 2-This test is checking the getter function for input shift
    print("___Plaintext Message Test 2___")
    print("Expected Output for Input Shift: 2")
    print("Actual Output for Input Shift:", first_encrypted_text.get_shift())
    

def test_encrypted_message():
    '''
    Write two test cases for the EncryptedMessage class here.
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what
    case(s) it is testing.
    '''

    # 1-This test is checking the decrypt_message function with punctuation
    print("___Encrypted Message Test 1___")
    encrypted_text = PlaintextMessage("hello!", 1)
    print("Encrypted Text: ", encrypted_text.get_encrypted_message_text())
    decrypted_text = EncryptedMessage(encrypted_text.get_encrypted_message_text())
    print("Expected Output for Decrypted Text: (1, 'hello!')")
    print("Actual Output for Decrypted Text: ", decrypted_text.decrypt_message())
    
    # 1-This test is checking the decrypt_message function with another input shift, space and numbers
    print("___Encrypted Message Test 2___")
    encrypted_text = PlaintextMessage("Today is March 8th", 25)
    print("Encrypted Text: ", encrypted_text.get_encrypted_message_text())
    decrypted_text = EncryptedMessage(encrypted_text.get_encrypted_message_text())
    print("Expected Output for Decrypted Text: (25, 'Today is March 8th')")
    print("Actual Output for Decrypted Text: ", decrypted_text.decrypt_message())
    

def decode_story():
    '''
    Write your code here to decode the story contained in the file story.txt.
    Hint: use the helper function get_story_string and your EncryptedMessage class.

    Returns: a tuple containing (best_shift, decoded_story)

    '''
    
    # Get the story and create an instance of EncryptedMessage 
    story_string = EncryptedMessage(get_story_string())
    
    return story_string.decrypt_message()

    

if __name__ == '__main__':

    # Uncomment these lines to try running your test cases
#     test_plaintext_message()
#     test_encrypted_message()

    # Uncomment these lines to try running decode_story_string()
     best_shift, story = decode_story()
     print("Best shift:", best_shift)
     print("Decoded story: ", story)
#    pass