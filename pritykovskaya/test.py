# coding=utf-8
import redis
import sys
from indexer import create_normalized_index, create_indexes
from search_runner import aggregate_tag_for_test, convert_tag_to_word_bag, aggregate_tag
import time
from searcher.PlainSearcher import PlainSearcher
from searcher.QuickSearcher import QuickSearcher
from utils import print_time


def test_searcher():
    searcher = PlainSearcher()
    tag = "galaxy gt i9001 plus s samsung отзыв"
    assert len(searcher.find_bag_of_words_for_tag(convert_tag_to_word_bag(tag, True))) == 12

def test_tag_aggregation():
    searcher = PlainSearcher()

    assert aggregate_tag_for_test(searcher, "000021 1 2 3 941 driving force gt logitech", True) ==\
           {'000021 1 2 3 941 driving force gt logitech*logitech driving force gt (941-000021)*1.00*1.00*0'}

    assert aggregate_tag_for_test(searcher, "ежики мылились 1 1 1 3 4 5", False) == set()

    assert aggregate_tag_for_test(searcher, "galaxy gt i9001 plus s samsung отзыв", True) == {
          'galaxy gt i9001 plus s samsung \xd0\xbe\xd1\x82\xd0\xb7\xd1\x8b\xd0\xb2*samsung gt-i9001 galaxy s plus 8gb, pure white*0.83*0.62*0',
          'galaxy gt i9001 plus s samsung \xd0\xbe\xd1\x82\xd0\xb7\xd1\x8b\xd0\xb2*samsung gt-i9001 galaxy s plus 8gb, ceramic white*0.83*0.62*0',
          'galaxy gt i9001 plus s samsung \xd0\xbe\xd1\x82\xd0\xb7\xd1\x8b\xd0\xb2*samsung gt-i9001 galaxy s plus 8gb, metallic black*0.83*0.62*0'}

    assert aggregate_tag_for_test(searcher, "black ericsson mini sony st15i xperia", True) == {
        'black ericsson mini sony st15i xperia*sony ericsson xperia mini st15i, white*0.83*0.83*0',
        'black ericsson mini sony st15i xperia*sony ericsson xperia mini st15i, black*1.00*1.00*0',
        'black ericsson mini sony st15i xperia*sony ericsson xperia mini pro sk17i, black*0.83*0.71*0',
        'black ericsson mini sony st15i xperia*sony ericsson xperia x10 mini (e10), doodles black*0.83*0.62*0'}

    assert aggregate_tag_for_test(searcher, "Стильный и функциональный пылесос от известного производителя!", False) == \
           {'\xd0\xa1\xd1\x82\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb8 \xd1\x84\xd1\x83\xd0\xbd\xd0\xba\xd1\x86\xd0\xb8\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xbf\xd1\x8b\xd0\xbb\xd0\xb5\xd1\x81\xd0\xbe\xd1\x81 \xd0\xbe\xd1\x82 \xd0\xb8\xd0\xb7\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb8\xd0\xb7\xd0\xb2\xd0\xbe\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f!*\xd0\xa1\xd1\x82\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb8 \xd1\x84\xd1\x83\xd0\xbd\xd0\xba\xd1\x86\xd0\xb8\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xbf\xd1\x8b\xd0\xbb\xd0\xb5\xd1\x81\xd0\xbe\xd1\x81 \xd0\xbe\xd1\x82 \xd0\xb8\xd0\xb7\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb8\xd0\xb7\xd0\xb2\xd0\xbe\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f!*1.00*1.00*1'}

    assert aggregate_tag_for_test(searcher, "Пылесосы и пылесборники", False) != set()

    assert aggregate_tag_for_test(searcher, "nikon Coolpix S8200", True) == {
        'nikon Coolpix S8200*nikon coolpix s8200, red*1.00*0.75*0',
        'nikon Coolpix S8200*nikon coolpix s8200, silver*1.00*0.75*0',
        'nikon Coolpix S8200*nikon coolpix s8200, black*1.00*0.75*0'}

    assert aggregate_tag_for_test(searcher, "8 blackbox xdevice видеорегистратор", True) == {
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-5 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-17 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-18 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-16 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-11 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-15 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80, silver*1.00*0.60*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-9 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-14 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80, white*1.00*0.60*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-6 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-20 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-12 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-4 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-1 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-15 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80, black*1.00*0.60*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-10 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*1.00*0.75*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-14 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80, black*1.00*0.60*0',
        '8 blackbox xdevice \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80*xdevice blackbox-11 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb5\xd0\xbe\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80 + \xd0\xb0\xd0\xba\xd0\xb2\xd0\xb0\xd0\xb1\xd0\xbe\xd0\xba\xd1\x81*1.00*0.60*0'}

    assert aggregate_tag_for_test(searcher, "325 clp", True) == {'325 clp*samsung clp-325*1.00*0.67*0'}

@print_time
def aggregate_tags_with_timing(searcher, tags, output):
    print "aggregate %d tags" % len(tags)
    for tag in tags:
        answers = aggregate_tag(searcher, tag, True)
        for answer in answers:
            output.write(answer + "\n")

def test_execution_time_plain_searcher():
    with open("2.5_tag", "r") as file:
        tags = map(str.strip, file.readlines())
    print("Finish reading")

    searcher = PlainSearcher()

    with open("test_res", "w") as output:
        current = []
        for tag in tags:
            current.append(tag)
            if len(current) == 100:
                aggregate_tags_with_timing(searcher, current, output)
                current = []
        aggregate_tags_with_timing(searcher, current, output)


def test_execution_time_quick_searcher():

    searcher = QuickSearcher()

    with open("2.5_tag", "r") as file:
        tags = map(str.strip, file.readlines())
    print("Finish reading")


    with open("test_res", "w") as output:
        current = []
        for tag in tags:
            current.append(tag)
            if len(current) == 100:
                aggregate_tags_with_timing(searcher, current, output)
                current = []
        aggregate_tags_with_timing(searcher, current, output)

if __name__ == "__main__":
    # setup()
    # test_searcher()
    # test_tag_aggregation()
    test_execution_time_quick_searcher()
