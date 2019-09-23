#!/usr/bin/env python3
import genanki
import requests

class ankibh:
    SPARQL_ENDPOINT = 'https://query.wikidata.org/sparql'

    bh_query = """
    SELECT ?bezirk ?bezirkLabel ?lpl WHERE {
    ?bezirk wdt:P31 wd:Q871419;
            wdt:P395 ?lpl;
            
    SERVICE wikibase:label { bd:serviceParam wikibase:language "de,en". }
    }
    """

    def __init__(self):
        self._genanki_setup()

    def _genanki_setup(self):
        bh_model = genanki.Model(
            1468421455, # keep static, generated with random.randrange(1 << 30, 1 << 31) as per genanki docs
            'BH Model',
            fields=[
                {'name': 'Autokennzeichen'},
                {'name': 'Name'},
            ],
            templates=[
                {
                    'name': 'Kennzeichen -> Name',
                    'qfmt': '<h3>{{Autokennzeichen}}</h3>',
                    'afmt': '<h4>{{Name}}</h4>',
                },
                {
                    'name': 'Name -> Kennzeichen',
                    'qfmt': '<h4>{{Name}}</h4>',
                    'afmt': '<h3>{{Autokennzeichen}}</h3>',
                }
            ]
        )

        self.bh_model = bh_model

        bh_deck = genanki.Deck(
            1468421456,
            'BHs in .at'
        )

        self.bh_deck = bh_deck


    def run(self):
        r = requests.get(self.SPARQL_ENDPOINT, params={'format': 'json', 'query': self.bh_query})
        data = r.json()

        for bezirk in data['results']['bindings']:
            lpl = bezirk['lpl']['value']
            name = bezirk['bezirkLabel']['value']
            if name.startswith('Bezirk '):
                name = name[7:]

            print(lpl, name)
            new_note = genanki.Note(
                self.bh_model,
                fields=[lpl, name]
            )
            self.bh_deck.add_note(new_note)

        genanki.Package(self.bh_deck).write_to_file('bhs.apkg')


if __name__ == '__main__':
    ourankibh = ankibh()
    ourankibh.run()