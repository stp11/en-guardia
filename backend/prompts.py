# flake8: noqa: E501
from models import Episode


def classification_prompt(
    episode: Episode, existing_categories: list[str] = None
) -> str:
    existing_categories_text = ""
    if existing_categories:
        existing_categories_text = f"""
        # CATEGORIES EXISTENTS
        Aquestes categories ja existeixen a la base de dades.
        Si el tema principal de l'episodi és conceptualment IDÈNTIC a una de les categories existents, utilitza aquesta categoria. Dona prioritat a les categories existents sempre que sigui possible per mantenir la consistència, fins i tot si el nom exacte no apareix en el text. Per exemple, si el text parla de "la revolta de 1640", i existeix la categoria "Guerra dels Segadors", has d'utilitzar "Guerra dels Segadors".
        {', '.join(existing_categories)}
        """

    return f"""
    # ROL
    Actua com un expert historiador i analista de dades.

    # TASCA
    A partir del titol i descripció proporcionats, extreu, classifica i estructura la informació històrica PRINCIPAL. Centra't en el títol primer per saber què és allò principal i exclou tot allò que sigui secundari de la descripció.
    Si no estàs segur d'una categoria, no l'assignis.
    Ignora qualsevol menció a convidats o experts del programa de ràdio i centra't exclusivament en el contingut històric.
    {existing_categories_text}

    # EXEMPLES
    ## EXEMPLE 1
    # TITOL
    La Guerra Civil a l'Alt Urgell i la Cerdanya
    # DESCRIPCIÓ
    Capítol 1211. Els anarquistes, especialment els sectors més durs, van assumir el poder i van substituir els ajuntaments legalment constituïts a les comarques de l'Alt Urgell i la Cerdanya després del cop d'estat militar del juliol del 1936. Tant a la Seu d'Urgell com a Puigcerdà es van viure episodis de violència i crueltat comesos per grups de persones que se suposava que defensaven la República. Entre d'altres, un dels anarquistes més destacats va ser l'anomenat Cojo de Málaga. En parlem amb l'historiador Josep Maria Solé i Sabaté i amb Pau Chica, màster en Història Contemporània i Món Actual per la Universitat de Barcelona i membre de l'Institut d'Estudis Comarcals de l'Alt Urgell.
    # SORTIDA JSON ESPERADA
    {{
        "temàtica": ["Guerra Civil Espanyola", "Anarquisme"],
        "època": ["Segle XX"],
        "personatges": ["Cojo de Málaga"],
        "localització": ["Alt Urgell", "Cerdanya"],
    }}

    ---
    # DADES A PROCESSAR
    # TITOL
    {episode.title}

    # DESCRIPCIÓ
    {episode.description}

    # FORMAT DE SORTIDA
    Proporciona la teva resposta exclusivament en format JSON RAW, sense cap formatació markdown ni blocs de codi.
    Si per a una clau no trobes cap informació rellevant, retorna una llista buida (per exemple, "personatges": []).
    Segueix aquesta estructura exacta:
    {{
        "temàtica": ["temàtica 1", "temàtica 2"],
        "època": ["època 1", "època 2"],
        "personatges": ["personatge 1", "personatge 2"],
        "localització": ["lloc 1", "lloc 2"],
    }}

    # INSTRUCCIONS ADDICIONALS
    - Utilitza la informació PRINCIPAL del títol per determinar la categoria temàtica. Pot haver-hi més d'una temàtica, les temàtiques secundàries s'extreuen de la descripció. Fes servir NOMS PROPIS o SINTAGMES NOMINALS com a categories (e.g. "Revolució Francesa", "Brigades Internacionals") i en el cas de personatges, fes servir nom i cognom (e.g. "Jean-Jacques Rousseau").
    - L'època hauria de ser el màxim de concreta possible, però NO ESPECIFIQUIS l'any. Sí que pots especificar el segle, però crea una categoria per cada segle. No especifiquis la part del segle, si el text diu "inicis del segle XX" o "finals del segle XIX" o "antiguitat tardana", hauria de ser "Segle XX" i "Segle XIX". Per exemple, si un fet passa durant la revolució francesa, hauria de ser "Revolució Francesa" i després èpoques addicionals que complementin la informació com ["Antic Règim", "Segle XVIII"].
    - Pels localització, ignora qualsevol localització que faci referència a convidats o experts convidats al programa de ràdio. Extreu les localitzacions rellevants que es mencionen a la descripció o títol.
    - Pels personatges, ignora qualsevol menció a convidats o experts del programa de ràdio, només aquells rellevants al fet històric. I fes servir el nom i cognom de cada personatge (e.g Jean-Jacques Rousseau enlloc de només Rousseau).
    - Per les categories temàtiques, associa "Catalunya" o "catalans" a la categoria QUAN SIGUI ESTRICTAMENT NECESSARI.
"""
