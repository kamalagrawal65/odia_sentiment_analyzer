# -*- coding: utf-8 -*-
from flask import Flask, request,render_template    #requests tell the type of request-get, post
import codecs
app = Flask(__name__)

odiadata=[]
tagged_data={}
negative_words=[]

@app.route('/')
def hello(methods = ['POST', 'GET']):
    if request.method=='POST':
      result = request.form
      print(result)
      return render_template("result.html",result = result)
    #else:
    return render_template("index.html",result = '')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      load_data()
      tag_data()
      result=final_result("ରାମ ଦୁଃଖ  ପିଲା |")
      return render_template("result.html",result = result)

def load_data():      
    global odiadata
    global negative_words
    for line in open("E:/ML/test/Senti_Wordnet- Part1.txt",encoding="utf8"):
        odiadata.append(line)

    for line in open("E:/ML/test/Senti_Wordnet- Part2.txt",encoding="utf8"):
        odiadata.append(line)
        
    for line in open("E:/ML/test/negative_words.txt",encoding="utf8"):
        negative_words.append(line)

def tag_data():
    global tagged_data
    for line in odiadata:
        text_data=line.split()
        odia_word=text_data[0]
        sentiment=text_data[2]
        polarity=text_data[3]
        
        tagged_data[odia_word]=(sentiment,polarity)
        
    #for tags in tagged_data.keys():
    #    senti_tuple=tagged_data[tags]
    #    print tags+" "+senti_tuple[0]+" "+senti_tuple[1]


def final_result(input_line):
    #All possible suffixes
    suffix=[]
    suffix.append('')
    suffix.append(['ଏ','ଇ','ଙ୍କ','ର'])
    suffix.append(['ଲା','ଙ୍କର','ଆ','ଛି','ତା','କୁ','ରେ'])
    suffix.append(['ଇଲା','ଉଛି'])
    
    if('|' in input_line):
        input_line=input_line.replace('|','')

    input_words=input_line.split()
    #for word in input_words:
    #    print word

    #Do the above for loop for the input_words
    final_polarity=0
    last_polarized_word_polarity=0

    for word in input_words:
        #stemming
        if(word in negative_words):
            final_polarity=(final_polarity-2*last_polarized_word_polarity)

        root_word=None
        for i in range(1,4):
            found=False
            root_word=word[:-i]
            suffix_word=word[-i:]
            if(suffix_word.encode('utf8') in suffix[i]):
                found=True

            #check for each root_word
            if((root_word.encode('utf8')) in tagged_data):
                senti_tuple=tagged_data[root_word.encode('utf8')]
                #print senti_tuple
                if(senti_tuple[0]=="Positive"):
                    last_polarized_word_polarity=float(senti_tuple[1])
                    final_polarity=final_polarity+float(senti_tuple[1])
                elif(senti_tuple[0]=="Negative"):
                    last_polarized_word_polarity=-1*float(senti_tuple[1])
                    final_polarity=final_polarity-float(senti_tuple[1])

        #check if given word is available
        if((word) in tagged_data):
            senti_tuple=tagged_data[word]
            if(senti_tuple[0]=="Positive"):
                last_polarized_word_polarity=float(senti_tuple[1])
                final_polarity=final_polarity+float(senti_tuple[1])
            elif(senti_tuple[0]=="Negative"):
                last_polarized_word_polarity=-1*float(senti_tuple[1])
                final_polarity=final_polarity-float(senti_tuple[1])
            #print tags+" "+senti_tuple[0]+" "+senti_tuple[1]

        #print final_polarity

    #print final_polarity

    if(final_polarity<0):
        return "Negative"
    elif(final_polarity>0):
        return "Positive"
    else:
        return "Neutral"


if __name__ == '__main__':
    app.run(debug = True, threaded=True)
