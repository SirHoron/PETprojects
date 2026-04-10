from .models import For_Card_Coctail
from django_redis import get_redis_connection
from lxml import etree

"""(name = "", category = "", type = "", ingredients = "", description = "", glass = "",
            strength = "", strengthprocent = 0, image = "", temperature = '', ctime = "", history = "", cooking = "")"""

redis_client = get_redis_connection(alias="default")

class Ingredient:
    """Класс для представления ингредиента коктейля"""
    def __init__(self, name: str, volume: str):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Ingredient('{self.name}', '{self.volume}')"

class Cocktail:
    """Класс для представления коктейля"""
    def __init__(self, name: str = "", category: str = "", type_: str = "", ingredients: list = [], description: str = "", glass: str = "",
                 strength: str = "", alcohol_percent: str = "", image_url: str = "", serving_temperature: str = "",
                 preparation_time: str = "", history: str = "", recipe_steps: list = []):
        self.name: str = name
        self.category: str = category
        self.type: str = type_
        self.ingredients: list[Ingredient] = ingredients       
        self.description: str = description
        self.glass: str = glass
        self.strength: str = strength
        self.alcohol_percent: str = alcohol_percent
        self.image_url: str = image_url
        self.serving_temperature: str = serving_temperature
        self.preparation_time: str = preparation_time
        self.history: str = history
        self.recipe_steps: list[str] = recipe_steps

    def __repr__(self):
        return f"Cocktail('{self.name}', category='{self.category}')"

def FCC_To_Coctail(*ar: For_Card_Coctail|dict) -> list[Cocktail]:
    if ar:
        coctails_list = []
        for FCC in ar:
            if type(FCC) == For_Card_Coctail:
                ingrs = []
                ingr = FCC.ingredients.split(";")
                for i in range(0, len(ingr)-1, 2):
                    ingrs.append(Ingredient(ingr[i], ingr[i+1]))
                coctails_list.append(Cocktail(FCC.name, FCC.category, FCC.type, ingrs, FCC.description,
                FCC.glass, FCC.strength, FCC.strengthprocent, FCC.image, FCC.temperature, FCC.ctime, FCC.history, FCC.cooking.split(";")))
            elif type(FCC) == dict:
                ingrs = []
                ingr = FCC["ingredients"].split(";")
                for i in range(0, len(ingr)-1, 2):
                    ingrs.append(Ingredient(ingr[i],ingr[i+1]))
                coctails_list.append(Cocktail(FCC["name"], FCC['category'], FCC['type'], ingrs, FCC['description'],
                FCC['glass'], FCC['strength'], FCC['strengthprocent'], FCC['image'], FCC['temperature'], FCC['ctime'], FCC['history'], FCC['cooking'].split(";")))
        return coctails_list
    return []

def _parse_cocktails(xml_file: str, limit: int = 6) -> list[Cocktail]:
    """
    Парсит XML-файл с коктейлями и возвращает список объектов Cocktail.
    :param xml_file: путь к XML-файлу
    :param limit: максимальное количество коктейлей для обработки
    :return: список объектов Cocktail
    """
    tree = etree.parse(xml_file)
    root = tree.getroot()

    cocktails = []
    # Находим все элементы cocktail
    for cocktail_elem in root.xpath('//cocktail')[:limit]:
        # Извлечение простых текстовых полей
        name = cocktail_elem.findtext('name', '').strip()
        category = cocktail_elem.findtext('category', '').strip()
        type_ = cocktail_elem.findtext('type', '').strip()
        description = cocktail_elem.findtext('description', '').strip()
        glass = cocktail_elem.findtext('glass', '').strip()
        strength = cocktail_elem.findtext('strength', '').strip()
        alcohol_percent = cocktail_elem.findtext('alcohol_percent', '0').strip()
        image_url = cocktail_elem.findtext('image_url', '').strip()
        serving_temperature = cocktail_elem.findtext('serving_temperature', '').strip()
        preparation_time = cocktail_elem.findtext('preparation_time', '').strip()
        history = cocktail_elem.findtext('history', '').strip()

        # Парсинг ингредиентов
        ingredients = []
        ingredients_elem = cocktail_elem.find('ingredients')
        if ingredients_elem is not None:
            for ing in ingredients_elem.findall('ingredient'):
                ing_name = ing.get('name', '').strip()
                ing_volume = ing.get('volume', '').strip()
                ingredients.append(Ingredient(ing_name, ing_volume))

        # Парсинг шагов рецепта
        recipe_steps = []
        recipe_elem = cocktail_elem.find('recipe')
        if recipe_elem is not None:
            for step in recipe_elem.findall('step'):
                step_text = step.text.strip() if step.text else ''
                recipe_steps.append(step_text)

        # Создаём объект Cocktail
        cocktail = Cocktail(
            name=name,
            category=category,
            type_=type_,
            ingredients=ingredients,
            description=description,
            glass=glass,
            strength=strength,
            alcohol_percent=alcohol_percent,
            image_url=image_url,
            serving_temperature=serving_temperature,
            preparation_time=preparation_time,
            history=history,
            recipe_steps=recipe_steps
        )
        cocktails.append(cocktail)

    return cocktails


def searching(type_, search) -> list[Cocktail|None]:
    data = []
    if type_ != "Все категории" or search != "none":
        if search != "none" and type_ != "Все категории":
            answ = [*For_Card_Coctail.objects.filter(category=type_, ingredients__icontains=search),
                    *For_Card_Coctail.objects.filter(category=type_, name__icontains=search)]
            data += answ
        elif search != "none":
            answ = [*For_Card_Coctail.objects.filter(ingredients__icontains=search), *For_Card_Coctail.objects.filter(name__icontains=search)]
            data += answ
        elif type_ != "Все категории":
            answ = [*For_Card_Coctail.objects.filter(category=type_)]
            data += answ
    else:
        data = For_Card_Coctail.objects.all()
    return FCC_To_Coctail(*data)

def MostPopular() -> list[Cocktail]:
    return _parse_cocktails("C:/Projects/MYprojects/Web_Bar/Web_BarCard/coctails.xml", limit=6)

def FindName(name) -> Cocktail:
    data = redis_client.hgetall(name)
    if not data:
        try:
            data = For_Card_Coctail.objects.filter(name=name)[0]
            redis_client.hset(data.name, mapping=dict((k, v) for k, v in data.__dict__.items() if k != '_state'))
            redis_client.expire(data.name, 600)
            return FCC_To_Coctail(data)[0]
        except Exception as e:
            print(e)
            return None
    data = dict((k.decode(), v.decode()) for k, v in data.items())
    return FCC_To_Coctail(data)[0]

def CreateCoctail(ingr, **data) -> bool:
    card = For_Card_Coctail.objects.create(name=data["name"], category=data["category"], type=data["type"], ingredients=ingr,\
        description=data["description"], glass=data["glass"], strength=data["strenght"], image=data["image"], temperature=data["tmre"], ctime=data["ctime"],\
        history=data["history"], cooking=data["cooking"], strengthprocent=data["strengthprocent"],)
    redis_client.hset(data["name"], mapping=card.__dict__)
    redis_client.expire(data["name"], 600)
    return True

def FindCategory(category: str, page: int, count: int = 12) -> tuple[list[Cocktail|None], int, int]:
    data = For_Card_Coctail.objects.filter(category=category)
    if data:
        lendata = len(data)
        pagescount = len(data)//count
        if len(data) >= count and page != pagescount+1:
            data = data[count*page-count:count*page]
        else:
            data = data[count*page-count:lendata]
        return (FCC_To_Coctail(*data), lendata, pagescount)
    else:
        return ([], 0, 0)