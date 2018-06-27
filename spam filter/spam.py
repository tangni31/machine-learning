import re
class keywordCounter:
    def __init__(self,keyword,spam,total_spam,legit,total_legit):
        self.keyword = keyword
        self.spam = spam
        self.total_spam = total_spam
        self.legit = legit
        self.total_legit = total_legit
        self.combin_probability = 0

def read_word(name):
    words = []
    lines = []
    with open(name,encoding='utf-8') as f:
        for line in f:
            line = line.replace('spam','').replace('ham','').strip()
            pat = re.compile('[^A-Za-z]+')
            words += pat.split(line)
    return words


def filter(content,keyword):
    flag = False
    if content.lower().find(keyword.lower())>0:
        flag = True
    return flag


#read words from training set
key_dic = {}
words = read_word('SMSSpamCollection')
for s in words:
    if s:
        key_dic[s] = keywordCounter(s,0,0,0,0)

mails = []
with open('SMSSpamCollection', encoding='utf-8') as f:
    for line in f:
        mails.append(line)
spam_number = 0
legit_number = 0
for mail in mails:
    if mail.startswith('spam'):
        for key in key_dic:
            flag = filter(mail,key)
            counter = key_dic[key]
            if flag:
                counter.spam += 1
            counter.total_spam += 1
        spam_number += 1
    else:
        for key in key_dic:
            flag = filter(mail,key)
            counter = key_dic[key]
            if flag:
                counter.legit += 1
            counter.total_legit += 1
        legit_number += 1


#remove those keywords that not highly related to the spam mails
need_remove = []
for key in key_dic:
    count = key_dic[key]
    if count.spam + count.legit == 0:
        need_remove.append(key)
        continue
    spam = 1.0 * count.spam / count.total_spam
    total_spam = 1.0 * count.total_spam / (count.total_spam + count.total_legit)
    legit = 1.0 * count.legit / count.total_legit
    total_legit = 1.0 * count.total_legit / (count.total_spam + count.total_legit)
    count.combin_probability = (spam * total_spam) / (spam * total_spam + legit * total_legit)
    if count.combin_probability < 0.92:
        need_remove.append(key)
for key in need_remove:
    key_dic.pop(key)



# testing our model
right = 0
wrong = 0
total_spam = 0
test_mail = []
with open('TestFile.txt') as f:
    for line in f:
        test_mail.append(line)
for mail in test_mail:
    if mail.startswith('spam'): total_spam+=1
    keywords = []
    for key in key_dic:
        flag = filter(mail,key)
        if flag:
            keywords.append(key)
    if len(keywords) <= 0: continue
    p1 = 1.0 * spam_number / (spam_number + legit_number)
    p2 = 1.0
    for k in keywords:
        count = key_dic[k]
        p1 *= count.spam / count.total_spam
        p2 *= (count.spam + count.legit) / (spam_number + legit_number)
    p = p1 / (p1 + p2)
    if p > 0.999 and mail.startswith('spam'):
        right += 1
    if p > 0.999 and mail.startswith('ham'):
        wrong += 1

print('total spam' + str(total_spam) + '   right prediction:' + str(right) )
print('accuracy:' + str(1.0*right/(right+wrong)))





