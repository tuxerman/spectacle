# -*- coding: UTF-8 -*-
"""
Fill primary DB with a bunch of submitted documents
"""
from spectacle.document.logic import add_document


def generate_dummy_data():
    # title, topic_id, content, summary, original_url, source
    return [
        {
            'title': 'The Wave Function',
            'topic_id': 100,
            'summary': '''Prof. Adams introduces wavefunctions as the fundamental quantity in describing quantum systems. Basic properties of wavefunctions are covered. Uncertainty and superposition are reiterated in the language of wavefunctions.''',
            'content': '',
            'original_url': 'https://ocw.mit.edu/courses/physics/8-04-quantum-physics-i-spring-2013/lecture-videos/lecture-3/Ei8CFin00PY.pdf',
            'source': 'MIT OCW'
        },
        {
            'title': 'Eigenstates of the Angular Momentum',
            'topic_id': 100,
            'summary': ''' Prof. Adams discusses energy degeneracy in 3D systems and its connection to rotational symmetry. The latter part of the lecture focuses on the angular momentum operators and their commutation relations.''',
            'content': '',
            'original_url': 'https://ocw.mit.edu/courses/physics/8-04-quantum-physics-i-spring-2013/lecture-videos/lecture-15/H5m39G-FAwE.pdf',
            'source': 'MIT OCW'
        },
        # TODO: The following fail in MySQL for some reason connected with unicode compatibility
        # {
        #     'title': 'Public Transport modal capacities and costs',
        #     'topic_id': 200,
        #     'summary': '''Cost modelling''',
        #     'content': '',
        #     'original_url': 'https://ocw.mit.edu/courses/civil-and-environmental-engineering/1-258j-public-transportation-systems-spring-2010/lecture-notes/MIT1_258JS10_lec03.pdf',
        #     'source': 'MIT OCW'
        # },
        # {
        #     'title': 'Environmental Regulation In Developing Economies',
        #     'topic_id': 300,
        #     'summary': '''Concludes our discussion of environmental issues in trade, growth, and development. Race to the Bottom/Trade. Environmental Kuznets Curves, Porter Hypothesis, Challenges in Environmental Regulation in Developing Economies''',
        #     'content': '',
        #     'original_url': 'https://ocw.mit.edu/courses/economics/14-42-environmental-policy-and-economics-spring-2011/lecture-notes/MIT14_42S11_note13.pdf',
        #     'source': 'MIT OCW'
        # },
    ]


def main():
    for new_doc_data in generate_dummy_data():
        print 'Adding doc with title: {}'.format(new_doc_data['title'])
        add_document(**new_doc_data)


if __name__ == '__main__':
    main()
