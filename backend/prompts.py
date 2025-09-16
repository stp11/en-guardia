# flake8: noqa: E501


def classification_prompt(title: str, description: str) -> str:
    return f"""
    # ROL
    Actua com un expert historiador i analista de dades.

    # TASCA
    A partir del titol i descripció proporcionats, extreu, classifica i estructura la informació històrica PRINCIPAL. Centra't en el títol primer per saber què és allò principal i exclou tot allò que sigui secundari de la descripció. Ignora qualsevol menció a convidats o experts del programa de ràdio i centra't exclusivament en el contingut històric.

    # TITOL
    {title}

    # DESCRIPCIÓ
    {description}

    # FORMAT DE SORTIDA
    Proporciona la teva resposta exclusivament en format JSON RAW, sense cap formatació markdown ni blocs de codi.
    Segueix aquesta estructura exacta:
    {{
        "epoca": ["epoca 1", "epoca 2"],
        "personatges_rellevants": ["personatge 1", "personatge 2"],
        "llocs_rellevants": ["lloc 1", "lloc 2"],
    }}

    # INSTRUCCIONS ADDICIONALS
    - Extreu la informació PRINCIPAL. Fes servir el text del títol per veure què és allò més important.
    - Si no s'esmenta cap personatge rellevant, el camp "personatges_rellevants" ha de ser una llista buida.
    - L'epoca hauria de ser el màxim de concreta possible. Per exemple, si un fet passa durant la revolució francesa, hauria de ser "revolució francesa" i després èpoques addicionals que complementin la informació com ["Antic Règim", "Segle XVIII"]. Si és una època prou coneguda, no cal que especifiquis els anys o segle.
    - Si no s'esmenta cap època, el camp "epoca" ha de ser una llista buida. - Si no s'esmenta cap lloc rellevant, el camp "llocs_rellevants" ha de ser una llista buida. En el cas anterior de "revolució francesa", el lloc rellevant hauria de ser "França".
    - Pels llocs_rellevants, ignora qualsevol localització que faci referència a convidats o experts convidats al programa de ràdio. Fes servir l'època extreta per saber quins son els llocs rellevants principals, ignora els secundaris.
    - Pels personatges, ignora qualsevol menció a convidats o experts del programa de ràdio, només aquells rellevants al fet històric.
"""
