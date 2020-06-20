
# Sample Test passing with nose and pytest
# Run with ```python -m pytest tests```

import pytest
import json
#import papernetwork

from papernetwork.papernetwork import PaperNetwork, Paper, PaperList

import copy

def test_pass():
    assert True, "dummy sample test"


def test_load_from_file():
    assert Paper(filename='tests/test_files/10.1038_SLASH_s41564-019-0626-z.json')['title'] == "Rapid MinION profiling of preterm microbiota and antimicrobial-resistant pathogens"
    my_paper = Paper()
    my_paper.load_from_file('tests/test_files/10.1038_SLASH_s41564-019-0626-z.json')
    assert my_paper['title'] == "Rapid MinION profiling of preterm microbiota and antimicrobial-resistant pathogens"

def test_load_from_file_two():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    assert my_paper['title'] == "title - a"
    assert my_paper['year'] == "2000"
    assert len(my_paper['references']) == 2
    assert len(my_paper['citations']) == 2


def test_load_url_ok():
    """ From jsonplaceholder.com retrieve a fake response to test the url part without overloading semantic scholar"""
    data = json.loads(Paper().load_url('https://jsonplaceholder.typicode.com/todos/1').read())
    assert data == {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

def test_load_url_fail():
    data = Paper().load_url('http://www.dnacoil.com/doesntwork')
    assert data is False

def test_append_wrong_type():
    with pytest.raises(Exception) as execinfo:
        my_network = PaperNetwork()
        my_network.collection.append('this is not a Paper object but a string')
    assert str(execinfo.value) == 'the item you are trying to add should be of the type Paper'


def test_append():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    my_network = PaperNetwork()
    my_network.collection.append(my_paper)

    assert my_paper in my_network.collection 
    assert my_paper2 not in my_network.collection 

def test_append_not_unique():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper_duplicate = Paper(filename='tests/test_files/paper-a.json')
    my_network = PaperNetwork()

    my_network.collection.append(my_paper)
    with pytest.raises(ValueError, match=r"This paperId is already present, only unique paperIds allowed"):
        my_network.collection.append(my_paper_duplicate)
        #print (my_network.collection)

def test_paper_equal():
    my_paper1 = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-a.json')
    my_paper3 = Paper(filename='tests/test_files/paper-k.json')

    assert my_paper1 == my_paper2
    assert my_paper1 != my_paper3


def test_update_paper_without_title():
    my_paper = Paper(filename='tests/test_files/paper-a.json')

    with pytest.raises(ValueError, match=r"Paper cannot have an empty title"):
        my_paper['title'] = ''

    with pytest.raises(ValueError, match=r"Paper cannot have an empty title"):
        del my_paper['title']

def test_update_paper_without_paperId():
    my_paper = Paper(filename='tests/test_files/paper-a.json')

    with pytest.raises(ValueError, match=r"Paper cannot have an empty paperId"):
        my_paper['paperId'] = ''

    with pytest.raises(ValueError, match=r"Paper cannot have an empty paperId"):
        del my_paper['paperId']


def test_update_paper_title_not_as_string():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    
    with pytest.raises(TypeError, match=r"title must be a string"):
        my_paper['title'] = 3

def test_update_paper_paperId_not_as_string():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    
    with pytest.raises(TypeError, match=r"paperId must be a string"):
        my_paper['paperId'] = 3


def test_setting_paper_directly():
    my_paper = Paper(data={"paperId":"q","title":"title - q","year":"2000"})
    assert my_paper['title'] == 'title - q'


def test_setting_paper_directly_without_title():
    with pytest.raises(ValueError, match=r"Paper cannot have an empty title"):
        my_paper = Paper(data={"paperId":"q","title":"","year":"2000"})
    

def test_copy():
    #my_paper = Paper(filename='tests/test_files/paper-a.json')
    #my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    my_network = PaperNetwork()

    with pytest.raises(TypeError, match=r"JSON argument needs to be a Paper or dict"):
        my_network._copy_paper_attributes_to_graph('foo node', 'a string not a dict or paper')

    with pytest.raises(ValueError, match=r"The node is not part of the graph, add the node first"):
        my_network._copy_paper_attributes_to_graph('foo node', {})

    with pytest.raises(TypeError, match=r"Node identifier needs to be a string, such as the paperId"):
        my_network._copy_paper_attributes_to_graph(2, {})


def test_paper_parse():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    my_network = PaperNetwork()
    my_network.collection.append(my_paper)
    my_network.collection.append(my_paper2)

    assert my_network.graph.size() == 6
    assert len(my_network.graph.nodes()) == 6 #-> ['title - x', 'title - a', 'title - y', 'title - b', 'title - c', 'title - k']
    assert my_network.graph.nodes['a']['year'] == "2000"
    assert my_network.graph.nodes['b']['year'] == "1990"
    assert my_network.graph.nodes['x']['year'] == "2003"

    assert my_network.graph.nodes['c']['year'] == "1991"
    assert my_network.graph.nodes['k']['year'] == "2005"
    assert my_network.graph.nodes['y']['year'] == "2011"


def test_paper_list_representations():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    list1 = PaperList([my_paper, my_paper2])
    
    assert list1.titles == ['title - a', 'title - k']
    assert list1.paperIds == ['a', 'k']


def test_paper_list():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    list1 = PaperList([my_paper])
    list2 = PaperList([my_paper])
    list3 = PaperList([my_paper2])
    assert list1 == list2
    assert list1 != list3
    list1 = PaperList([my_paper, my_paper2])
    list2 = PaperList([my_paper, my_paper2])
    list3 = PaperList([my_paper2, my_paper])
    assert list1 == list2
    assert list1 != list3  # PaperList is a  List and not a Set, so these are not equal

def test_paper_list_two():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    listA = PaperList([my_paper, my_paper2])
    listB = copy.deepcopy(listA)

    assert listA == listB

    listA[0]['new key'] = 'makes listA and listB not the same'

    assert listA != listB

    #not_a_paper_list = []
    #with pytest.raises(TypeError, match=r"Node identifier needs to be a string, such as the paperId"):
    #    if list1 != "not_a_paper_list":
    #        pass


def test_paper_parse_two():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    my_network = PaperNetwork()
    my_network.collection.append(my_paper)
    my_network.collection.append(my_paper2)

    #my_network.parse_papers()

    assert my_network.graph.size() == 6
    assert len(my_network.graph.nodes()) == 6  #-> ['title - x', 'title - a', 'title - y', 'title - b', 'title - c', 'title - k']
    assert my_network.graph.nodes['a']['year'] == "2000"
    assert my_network.graph.nodes['b']['year'] == "1990"
    assert my_network.graph.nodes['x']['year'] == "2003"


    my_network.collection.remove(my_paper2)

    assert my_network.graph.size() == 4
    assert len(my_network.graph.nodes()) == 5


    # Testing the deepcopy function. Everytime we access the graph, we need to check whether the collection changed
    assert my_network.graph.nodes[my_network.collection[0]['paperId']]['year'] == my_network.collection[0]['year']
    my_network.collection[0]['year'] = "9999"
    assert my_network.graph.nodes[my_network.collection[0]['paperId']]['year'] == my_network.collection[0]['year'] # Test that the deepcopy of the Paperlist is functioning
    assert my_network.graph.size() == 4


def test_load_from_semantic_scholar_wrong_doi():
    with pytest.raises(Exception) as execinfo:
        data = Paper().load_from_semantic_scholar('doidoesnotexcist')
    assert str(execinfo.value) == 'Download failed'

# While devving keep this live connection to s_s out
def test_load_from_semantic_scholar():
    data = Paper()
    data.load_from_semantic_scholar('10.1093/nar/gkw1328')
    assert data['title']=='Rapid resistome mapping using nanopore sequencing'

    data2 = Paper(doi='10.1093/nar/gkw1328')
    assert data2['title']=='Rapid resistome mapping using nanopore sequencing'

def test_paper_json():
    my_paper = Paper(filename='tests/test_files/paper-a.json')
    my_paper2 = Paper(filename='tests/test_files/paper-k.json')
    my_network = PaperNetwork()
    my_network.collection.append(my_paper)
    my_network.collection.append(my_paper2)


    assert my_network.calculate_json() == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - y', 'year': '2011', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 0, 'corpus': 5, 'out_degree': 1, 'id': 'y'}, {'title': 'title - b', 'year': '1990', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 0, 'out_degree': 0, 'id': 'b'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'b'}, {'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'y', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}

    # these three cases should not  change the output
    assert my_network.calculate_json(mimimum_citation_count_of_references=1) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - y', 'year': '2011', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 0, 'corpus': 5, 'out_degree': 1, 'id': 'y'}, {'title': 'title - b', 'year': '1990', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 0, 'out_degree': 0, 'id': 'b'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'b'}, {'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'y', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}
    assert my_network.calculate_json(mimimum_citation_count_of_references=1, minimum_times_citing_collection=1) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - y', 'year': '2011', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 0, 'corpus': 5, 'out_degree': 1, 'id': 'y'}, {'title': 'title - b', 'year': '1990', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 0, 'out_degree': 0, 'id': 'b'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'b'}, {'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'y', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}
    assert my_network.calculate_json(minimum_times_citing_collection=1) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - y', 'year': '2011', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 0, 'corpus': 5, 'out_degree': 1, 'id': 'y'}, {'title': 'title - b', 'year': '1990', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 0, 'out_degree': 0, 'id': 'b'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'b'}, {'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'y', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}

    # with restrictions
    assert my_network.calculate_json(mimimum_citation_count_of_references=2) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - y', 'year': '2011', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 0, 'corpus': 5, 'out_degree': 1, 'id': 'y'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'y', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}
    assert my_network.calculate_json(minimum_times_citing_collection=2) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 2, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - x', 'year': '2003', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 1, 'corpus': 5, 'out_degree': 1, 'id': 'x'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'c'}, {'source': 'x', 'target': 'a'}, {'source': 'k', 'target': 'x'}, {'source': 'k', 'target': 'c'}]}

    # double restrictions
    assert my_network.calculate_json(mimimum_citation_count_of_references=2, minimum_times_citing_collection=2 ) == {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'title': 'title - a', 'year': '2000', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 1, 'corpus': 1, 'out_degree': 0, 'id': 'a'}, {'title': 'title - c', 'year': '1991', 'url': [], 'authors': [], 'venue': [], 'warning': [], 'in_degree': 2, 'corpus': 0, 'out_degree': 0, 'id': 'c'}, {'title': 'title - k', 'year': '2005', 'url': [], 'authors': [], 'venue': [], 'warning': ['Serious warning: reference list seems very short (<10)', 'Note: seems like not widely cited (<5)'], 'in_degree': 0, 'corpus': 1, 'out_degree': 0, 'id': 'k'}], 'links': [{'source': 'a', 'target': 'c'}, {'source': 'k', 'target': 'c'}]}


def test_pn_init():
    list_of_jsons = ['tests/test_files/paper-a.json', 'tests/test_files/paper-k.json']
    my_network = PaperNetwork(filename_list=list_of_jsons)
    assert len(my_network.collection) == 2

# Turns of while devving
    list_of_dois = ['10.1093/nar/gkw1328']
    my_network = PaperNetwork(filename_list=list_of_jsons, doi_list=list_of_dois)
    assert len(my_network.collection) == 3

def test_init_fail_both():
    with pytest.raises(Exception) as execinfo:
        Paper(filename='foo', doi='bar')
    assert str(execinfo.value) == 'Cannot use both filename and doi to retreive paper'
    
def test_load_url_fail():
    Paper().load_url('https://jsonplaceholder.typicode.com/todos/1')
    