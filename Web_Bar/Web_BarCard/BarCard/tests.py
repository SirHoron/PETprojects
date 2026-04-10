from .models import For_Card_Coctail
from lxml import etree

def parse_cocktails(xml_file: str):
    """
    Парсит XML-файл с коктейлями и возвращает список объектов Cocktail.
    :param xml_file: путь к XML-файлу
    :param limit: максимальное количество коктейлей для обработки
    :return: список объектов Cocktail
    """
    
    tree = etree.parse(xml_file)
    root = tree.getroot()
    # Находим все элементы cocktail
    for cocktail_elem in root.xpath('//cocktail'):
        with open("C:/Projects/MYprojects/Web_Bar/Web_BarCard/names.txt", "r", encoding="utf-8") as r:
            names = r.read().split(",")
        # Извлечение простых текстовых полей
        
        name = cocktail_elem.findtext('name', '').strip()
        if name in names:
            continue
        else:
            with open("C:/Projects/MYprojects/Web_Bar/Web_BarCard/names.txt", "a", encoding="utf-8") as w:
                w.write(f",{name}")
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
                ingredients.append(f"{ing_name};{ing_volume}")
        # Парсинг шагов рецепта
        recipe_steps = []
        recipe_elem = cocktail_elem.find('recipe')
        if recipe_elem is not None:
            for step in recipe_elem.findall('step'):
                step_text = step.text.strip() if step.text else ''
                recipe_steps.append(step_text)
        # Создаём объект Cocktail
        cocktail = For_Card_Coctail.objects.create(name = name, category = category, type = type_, ingredients = ";".join(ingredients), description = description, glass = glass,
            strength = strength, strengthprocent = int(alcohol_percent), image = image_url, temperature = serving_temperature, ctime = preparation_time, history = history, cooking = ";".join(recipe_steps))
    with open("C:/Projects/MYprojects/Web_Bar/Web_BarCard/names.txt", "r", encoding="utf-8") as r:
        names = r.read().split(",")