from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]    
    all_words = []       
    for mail in emails:    
        with open(mail) as m:
            for i,line in enumerate(m):
                if i == 2:  #Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words
    
    dictionary = Counter(all_words)
    print(dictionary)
    # Paste code for non-word removal here(code snippet is given below) 
    list_to_remove = dictionary.keys()
    for item in list(list_to_remove):
        if item.isalpha() == False: 
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)
    return dictionary
def extract_features(mail_dir,dictionary):
    print("in") 
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID][wordID] = words.count(word)
        docID = docID + 1     
    return features_matrix

def extract_single(mail_file):
    features_matrix = np.zeros((len(files),3000))
    fil=mail_file
    docID = 0;
    with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1 
    return features_matrix
        


def spamornot(filetest):
    # Create a dictionary of words with its frequency
    
    train_dir = '/Users/rashmitharavichandran/Downloads/ling-spam/train-mails'
    dictionary = make_Dictionary(train_dir)
    
    # Prepare feature vectors per training mail and its labels
    
    train_labels = np.zeros(702)
    train_labels[351:701] = 1
    train_matrix = extract_features(train_dir,dictionary)
    
    # Training SVM and Naive bayes classifier
    
    model1 = MultinomialNB()
    model2 = LinearSVC()
    model1.fit(train_matrix,train_labels)
    model2.fit(train_matrix,train_labels)
    
    # Test the unseen mails for Spam
    
    test_sample=filetest
    tessam=extract_features(test_sample,dictionary)
    result=model1.predict(tessam)
    print(result)
    
    if(result==1.):
        return "spam"
    else:
        return "ham"

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        fi="/Users/rashmitharavichandran/myth/testsample/"
        with open(fi+"samtest","w") as file:
            file.write(uploaded_file_url)

        final=spamornot(fi)
        # filename=request.session['url']
        # fl='.'+filename
        print(final)
        return render(request, 'index.html', {
            'uploaded_file_url': final
        })
    return render(request, 'index.html')