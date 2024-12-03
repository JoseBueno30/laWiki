import copy
import json

import mwparserfromhell
import pypandoc
from jinja2.lexer import newline_re

body = '<mapframe lat="48.8566" lon="2.3522" zoom="12" markers="[{&quot;lat&quot;:48.857,&quot;lon&quot;:2.352,&quot;label&quot;:&quot;Marker 1&quot;}]"></mapframe>'
body2= "<mapframe lat=4401490.346984346 lon=-497548.6089364281 zoom=13 markers=[{lat=-497548.6089364281, lon=4401490.346984346}]></mapframe>"
body3= '<mapframe lat="48.8566" lon="2.3522" zoom="12" markers="[{"lat":48.857,"lon":2.352}]"></mapframe>'
objective='<MapView lat="48.8566" lon="2.3522" zoom="12" markers={[{"lat":48.857,"lon":2.352}, {"lat":48.957,"lon":2.452}]}/>'
obj2 = """<h1>Dynamic Article</h1>
    <p>This is some text before the map:</p>
    <MapView lat="48.8566" lon="2.3522" zoom="12"
        markers={[{"lat":48.857,"lon":2.352}, {"lat":49.857,"lon":3.352}]}
    />
    <p>More content here.</p>"""
#TODO: BUG WHIT VARIOUS MARKERS
test = """= Historia de Anuel AA =

'''Anuel AA''' (nombre real: Emmanuel Gazmey Santiago; 26 de noviembre de 1992) es un cantante y rapero puertorriqueño conocido por ser una de las figuras principales del trap latino.

== Inicios de su carrera ==

Anuel comenzó su carrera musical en 2010, publicando canciones de estilo urbano que ganaron popularidad en plataformas digitales. Su primer éxito significativo fue en 2016, consolidando su lugar en el género.

=== Influencias y estilo ===

Su música mezcla:
* Temas de la vida urbana y callejera.
* Ritmos de trap y reguetón.
* Colaboraciones con artistas internacionales.

== Controversias ==

* En 2016, Anuel enfrentó problemas legales, lo que lo llevó a prisión por posesión de armas.
* Durante su encarcelamiento, continuó lanzando música, logrando mantener su relevancia en la industria.

== Legado ==

Anuel es reconocido como uno de los pioneros del trap latino y un ícono cultural, con millones de seguidores alrededor del mundo.

 <MapView lat="36.728064009663825" lon="-4.4715638324535965" zoom="16" markers={[{"lat":-4.4695552,"lon":36.72965120000002},{"lat":-4.474584863620265,"lon":36.728661088149366},{"lat":-4.4705132363472035,"lon":36.72645526954372},]}/>"""

body_translated = copy.deepcopy(test)

body_translated = mwparserfromhell.parse(body_translated)

# print(body_translated)

for tag in body_translated.ifilter_tags(matches=lambda t: t.tag == "MapView"):
    # print(type(tag))
    # print(tag.self_closing)

    lat = tag.get("lat")
    lon = tag.get("lon")
    zoom = tag.get("zoom")
    markers = tag.get("markers")

    # print(markers)

    # Wrap the MapView in a div
    mapview_html = (

        f"<MapView {lat} {lon} {zoom} {markers}/>"

    )


    # print(mapview_html)
    # f"markers='{json.dumps(markers_data).replace('\"', '&quot;')}' "

    # Create MapComponent placeholder
    # map_component = f"<MapComponent data='{json.dumps(attributes)}' />"
    # body_translated.replace(str(tag), mapview_html)

    # print(body_translated)


body_translated = pypandoc.convert_text(body_translated, to='html', format='mediawiki')
print(body_translated)