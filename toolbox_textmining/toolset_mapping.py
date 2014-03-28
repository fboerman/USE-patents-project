__author__ = 'williewonka'

class ToolBox:
    # sentenceweight = 5
    searchwidth = 5
    def __init__(self, encoding):
        #constructor, reads and stores the encoding of the toolset in a list of dictionaries
        #every item in list represents a sentence
        #the sentence itself is a dictionary with words as keys and weight as values
        self.sentences = []
        for entry in encoding.split("%"):#split on the sentences
            if entry == "" or entry == " ":
                continue
            sentence = {
                "weight" : entry.split("$")[1]
            }
            line = entry.split("$")[0]
            for word in line.split(" "):
                if word == "":#skip empty entries cause by double spacing
                    continue
                sentence[word.split('|')[0]] = float(word.split('|')[1]) #save the word and weight
            if sentence:
                self.sentences.append(sentence) #save the sentence

    def Check(self, line):
        #checks the line against the encoding (line already split)
        #looks also around the words to check for sentences
        #returns the weight for the specific toolbox
        #check word for word and crossreference to the encoding
        #the total weight
        weight = 0
        #keep track of index so that jumping is possible
        i = 0
        while i < len(line):
            word = line[i]
            #iterate through the sentences and check the word
            for sentence in self.sentences:
                #iterate through all the words
                temp_weight = self.CheckSentence(word,sentence)
                #if the word is hit in this sentence, look around to check for other parts of sentence
                if temp_weight > 0:
                    #clip the search line to keep within the line
                    z = i - self.searchwidth
                    if z < 0:
                        z = 0
                    end = i + self.searchwidth
                    if end > len(line):
                        end = len(line)
                    while z < end:
                        if i == z:
                            z += 1
                            continue
                        result = self.CheckSentence(line[z],sentence)
                        if result > 0:

                            #apply sentence weight
                            if result > temp_weight:
                                temp_weight = result
                            temp_weight *= sentence["weight"]
                            break
                        z += 1
                #ready with sentence checking, apply the weight
                weight += temp_weight
            i += 1
        return round(weight,1)


    def CheckSentence(self, word, sentence): #checks the sentence, returns weight
        if word == "":
            return 0
        for keyword in list(sentence.keys()):
            if keyword.lower() in word.lower() and keyword.lower() is not "weight":
                return sentence[keyword]
        return 0
