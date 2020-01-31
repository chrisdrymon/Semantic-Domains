import string
import os
import xml.etree.ElementTree as ET

pos0_dict = {'a': 'adj', 'n': 'noun', 'v': 'verb', 'd': 'adv', 'c': 'conj', 'g': 'conj', 'r': 'adposition', 'b': 'conj',
             'p': 'pronoun', 'l': 'article', 'i': 'interjection', 'x': 'other', 'm': 'numeral', 'e': 'interjection'}
pos4_dict = {'i': 'indicative', 's': 'subjunctive', 'n': 'infinitive', 'm': 'imperative', 'p': 'participle',
             'o': 'optative'}
agdt2_rel_dict = {'obj': 'object'}
proiel_pos_dict = {'A': 'adj', 'D': 'adv', 'S': 'article', 'M': 'numeral', 'N': 'noun', 'C': 'conj', 'G': 'conj',
                   'P': 'pronoun', 'I': 'interjection', 'R': 'adposition', 'V': 'verb'}


def deaccent(dastring):
    """Returns an unaccented version of dastring."""
    aeinput = "άἀἁἂἃἄἅἆἇὰάᾀᾁᾂᾃᾄᾅᾆᾇᾰᾱᾲᾳᾴᾶᾷἈἉΆἊἋἌἍἎἏᾈᾉᾊᾋᾌᾍᾎᾏᾸᾹᾺΆᾼέἐἑἒἓἔἕὲέἘἙἚἛἜἝΈῈΈ"
    aeoutput = "ααααααααααααααααααααααααααΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑΑεεεεεεεεεΕΕΕΕΕΕΕΕΕ"
    hoinput = "ΉῊΉῌἨἩἪἫἬἭἮἯᾘᾙᾚᾛᾜᾝᾞᾟήἠἡἢἣἤἥἦἧὴήᾐᾑᾒᾓᾔᾕᾖᾗῂῃῄῆῇὀὁὂὃὄὅόὸόΌὈὉὊὋὌὍῸΌ"
    hooutput = "ΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗΗηηηηηηηηηηηηηηηηηηηηηηηηοοοοοοοοοΟΟΟΟΟΟΟΟΟ"
    iuinput = "ΊῘῙῚΊἸἹἺἻἼἽἾἿΪϊίἰἱἲἳἴἵἶἷΐὶίῐῑῒΐῖῗΫΎὙὛὝὟϓϔῨῩῪΎὐὑὒὓὔὕὖὗΰϋύὺύῠῡῢΰῦῧ"
    iuoutput = "ΙΙΙΙΙΙΙΙΙΙΙΙΙΙιιιιιιιιιιιιιιιιιιιΥΥΥΥΥΥΥΥΥΥΥΥυυυυυυυυυυυυυυυυυυυ"
    wrinput = "ώὠὡὢὣὤὥὦὧὼώᾠᾡᾢᾣᾤᾥᾦᾧῲῳῴῶῷΏὨὩὪὫὬὭὮὯᾨᾩᾪᾫᾬᾭᾮᾯῺΏῼῤῥῬ"
    wroutput = "ωωωωωωωωωωωωωωωωωωωωωωωωΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩΩρρΡ"
    # Strings to feed into translator tables to remove diacritics.

    aelphas = str.maketrans(aeinput, aeoutput, "⸀⸁⸂⸃·,.—")
    # This table also removes text critical markers and punctuation.

    hoes = str.maketrans(hoinput, hooutput, string.punctuation)
    # Removes other punctuation in case I forgot any.

    ius = str.maketrans(iuinput, iuoutput, '0123456789')
    # Also removes numbers (from verses).

    wros = str.maketrans(wrinput, wroutput, string.ascii_letters)
    # Also removes books names.

    return dastring.translate(aelphas).translate(hoes).translate(ius).translate(wros).lower()


def denumber(dalemma):
    """Removes number from the string dalemma."""

    numers = str.maketrans('', '', '01234567890')

    return dalemma.translate(numers)


def resequence():
    """Numbers each word element in a treebank with a unique sequential id starting from 1. Then adjusts
    head-ids to match the new numbering."""
    os.chdir('/home/chris/Desktop/CustomTB')
    indir = os.listdir('/home/chris/Desktop/CustomTB')
    worddict = {}

    # This will create a dictionary matching old ID's to their new ones so heads can be reassigned
    # then it will assign the new sequential IDs.
    for file_name in indir:
        i = 1
        if not file_name == 'README.md' and not file_name == '.git':
            print(file_name)
            tb = ET.parse(file_name)
            tbroot = tb.getroot()
            if tbroot.tag == 'treebank':
                for body in tbroot:
                    for sentence in body:
                        for word in sentence:
                            if word.tag == 'word':
                                sentenceid = str(sentence.get('id'))
                                wordid = str(word.get('id'))
                                sentwordid = str(sentenceid + '-' + wordid)
                                worddict[sentwordid] = i
                                word.set('id', str(i))
                                i += 1

                # This will assign new head ID's that are in accordance with the new numbering system.
                for body in tbroot:
                    for sentence in body:
                        for word in sentence:
                            if word.tag == 'word':
                                sentenceid = str(sentence.get('id'))
                                headid = str(word.get('head'))
                                sentheadid = str(sentenceid + '-' + headid)
                                if sentheadid in worddict:
                                    newheadid = worddict[sentheadid]
                                    word.set('head', str(newheadid))

                tb.write(file_name, encoding="unicode")
                print("Resequenced:", file_name)

            if tbroot.tag == 'proiel':
                for source in tbroot:
                    for division in source:
                        for sentence in division:
                            for token in sentence:
                                if token.tag == 'token':
                                    sentenceid = str(sentence.get('id'))
                                    wordid = str(token.get('id'))
                                    sentwordid = str(sentenceid + '-' + wordid)
                                    worddict[sentwordid] = i
                                    token.set('id', str(i))
                                    i += 1

                for source in tbroot:
                    for division in source:
                        for sentence in division:
                            for token in sentence:
                                if token.tag == 'token':
                                    sentenceid = str(sentence.get('id'))
                                    headid = str(token.get('head-id'))
                                    sentheadid = str(sentenceid + '-' + headid)
                                    if sentheadid in worddict:
                                        newheadid = worddict[sentheadid]
                                        token.set('head-id', str(newheadid))

                tb.write(file_name, encoding="unicode")
                print("Resequenced:", file_name)


# This returns the head of the word
def header(f_sentence, f_word):
    return_head = 'no head'
    f_head_id = 0
    if f_word.has_attr('head'):
        f_head_id = f_word['head']
    if f_word.has_attr('head-id'):
        f_head_id = f_word['head-id']
    for f_head in f_sentence:
        if f_head.has_attr('id'):
            if f_head['id'] == f_head_id:
                return_head = f_head
    return return_head


# This returns the part-of-speech or the mood if the part-of-speech is a verb for a given word.
def poser(f_word):
    if f_word.has_attr('postag'):
        if len(f_word['postag']) > 0:
            pos0 = f_word['postag'][0]
            if pos0 in pos0_dict:
                f_pos = pos0_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['postag']) > 4:
                        pos4 = f_word['postag'][4]
                        if pos4 in pos4_dict:
                            f_pos = pos4_dict[pos4]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    elif f_word.has_attr('part-of-speech'):
        if len(f_word['part-of-speech']) > 0:
            pos0 = f_word['part-of-speech'][0]
            if pos0 in proiel_pos_dict:
                f_pos = proiel_pos_dict[pos0]
                if f_pos == 'verb':
                    if len(f_word['morphology']) > 3:
                        pos3 = f_word['morphology'][3]
                        if pos3 in pos4_dict:
                            f_pos = pos4_dict[pos3]
            else:
                f_pos = 'other'
        else:
            f_pos = 'other'
    else:
        f_pos = 'other'
    return f_pos


# Given the sentence find_all list and a head word, this function returns the words which depend on that head.
def give_dependents(sentence_words, head_word):
    the_words = []
    if head_word.has_attr('id'):
        head_word_id = head_word['id']
        for f_word in sentence_words:
            if f_word.has_attr('head'):
                word_head = f_word['head']
                if word_head == head_word_id:
                    the_words.append(f_word)
            if f_word.has_attr('head-id'):
                word_head = f_word['head-id']
                if word_head == head_word_id:
                    the_words.append(f_word)
    return the_words
