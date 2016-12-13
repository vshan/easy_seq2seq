from intializations import *

def redditQuery(que):
    print "Querying reddit"
    titles = []
    comments = []
    subreddit = reddit.subreddit('askreddit')
    submissions = subreddit.search(query=que, limit=1)
    for submission in submissions:
        comments = list(submission.comments)

    comments = comments[:50]
    comments = [x.body for x in comments]
    # print len(comments)
    # for submission in submissions:
    #     titles.append(submission.title)
    # chos_sub = process.extractOne(que, titles)
    # # return chos_sub[0]
    # for submission in submissions:
    #     if submission.title == titles[0]:
    #         comments = list(submission.comments)
    # print len(comments)
    # print(comments)
    chos_comm = process.extractOne(que, comments)
    # print chos_comm
    return chos_comm[0]

## Method to preprocess the sentence by making neccesary replacements and formatting unncecssary symbols
def preprocess(sent):
    sentence_list = sent.split()
    new_sentence = []

    for word in sentence_list:
        if word[-1] == "?":
            word = word[:-1]
        for candidate_replacement in replacements:
            if candidate_replacement in word:
                word = word.replace(candidate_replacement, replacements[candidate_replacement])
        new_sentence.append(word)

    return " ".join(new_sentence)

## Method to remove stop words
def removeStop(sent):
    filtered_words = [w for w in sent.split() if not w in stop]
    filtered_sent = " ".join(filtered_words)
    #print filtered_words
    return filtered_sent

## Method to determine if the given NL command is a Question or Statement
def isQuestion(question):
    try:
        qWord = None
        part_q = filter(None, re.split("[,\-!?:.]+", question))
        for que in part_q:
            words = word_tokenizer.tokenize(que)
            if words[0].lower() in qWords:
                qWord = words[0].lower()
        if qWord:
            return qWord
        else:
            return ''
    except:
        print "Error occured at isQuestion."

## Method to get neccesary keywords to query
def getKeywords(arg,sent):
    q = []
    sent = word_tokenizer.tokenize(removeStop(sent))
    for w in sent:
        if w.lower() not in arg:
            q.append(w)
    return q

## Method to query the local knowledge base and get a repy if possible
def queryKB(que, keys):
    print "Querying Knowledge Base"
    print "The keys are " + str(keys)
    with open('Knowbase.json') as data_file:
        KB_JSON = json.load(data_file)
    #print KB_JSON
    if que.lower() not in KB_JSON:
        return False
    X = KB_JSON[que.lower()]
    if not keys:
        try:
            return X['default']
        except:
            return False
    #print X
    should_restart = True
    hit = False
    while should_restart:
        should_restart = False
        for i in keys:
            try:
                if i.lower() in X:
                    X = X[i.lower()]
                    keys.remove(i)
                    if not keys:
                        hit = True
                    should_restart = True
                    break
            except:
                break
    if(hit):
        try:
            return X['default']
        except:
            return X
    else:
        return False

## Method to determine whether query is WIKI type or REDDIT
def queryType(sent):
    sent = tagger.tag(word_tokenizer.tokenize(sent))
    print sent
    for w  in sent:
        if(w[0] not in stop and w[0] not in qWords and "N" not in w[1] ):
            print w
            return "REDDIT"
    return "WIKI"

## Method to get info from Wiki API
def getInformation(keys):
    print "Querying Wiki"
    info = ""
    key = " ".join(keys)
    info = getWikiKnow(key)
    return info

## Utility method to extract knowledge from wiki API
def getWikiKnow(key):
    res = wikipedia.search(key)
    chosen_page = res[0]
    if "disambiguation" in chosen_page:
        chosen_page = res[1]
    cont = wikipedia.page(chosen_page)
    return cont.content.split('\n')

def unintelligble(sent):
    return (('_UNK' in sent) or ('What ?' in sent) or ('I don \' t know .' in sent))

def has_NNP(keys):
    a = nltk.pos_tag(keys)
    a = [x[1] for x in a]
    return ('NNP' in a)


## Main method to process the query and get a reply
def reply(sent, bot_reply):
    sent = preprocess(sent)
    # print sent
    reply = bot_reply
    if unintelligble(reply):
        word = isQuestion(sent)
        keys = getKeywords(word, sent)
        if word != '' and has_NNP(keys):
            info = getInformation(keys)
            reply = nltk.tokenize.sent_tokenize(info[0])[0]
        else:
            reply = redditQuery(sent)
    return reply
    # if(word):
    #     print word
    #     rep = queryKB(word, getKeywords(word, sent))
    #     if(rep):
    #         return rep
    #     else:
    #         qType = queryType(sent)
    #         if(qType == "WIKI"):
    #             keys = getKeywords(word, sent)
    #             info = getInformation(keys)
    #             return info[0]
    #         elif(qType == "REDDIT"):
    #             return redditQuery(sent)
    #         # keys = getKeywords(word, sent)
    #         # info = getInformation(keys)
    #         # reply += "Factually speaking...\n"
    #         # reply += info[0].split('.')[0]
    #         # reply += "\n\nBUT since you asked:\n"
    #         # reply += redditQuery(sent)
    #         # return reply
    # else:
    #     return 'Statement'

## Driver
# while True:
#     rep = reply(raw_input("Enter: "))
#     print ">>>>>\n"
#     print rep
#     print "\n>>>>>"
