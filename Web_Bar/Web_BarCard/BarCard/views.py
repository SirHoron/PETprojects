from django.shortcuts import render
from django.http import HttpRequest
from .services import CreateCoctail, FindCategory, FindName, MostPopular, searching, Ingredient
from .markingformer import cardformer, pages_block, CookingSteps, ingredients_steps


"""  Страницы  """
def main(request):
    data = MostPopular()
    return render(request, "main.html", {"coctails": cardformer(data)})

def IBA(request: HttpRequest):
    page = int(request.get_full_path().split("/")[2][5:])
    desc = ''
    unforg = ''
    newera = ''
    modern = ''
    typec = ''
    try:
        type = request.GET["type"]
    except KeyError:
        type = "unforgettable"

    match type:
        case "unforgettable":
            desc = "Исторические классические коктейли, которые выдержали испытание временем и остаются популярными десятилетиями."
            typec = "Незабываемые"
            unforg = "active"
        case "modern":
            desc = "Коктейли, созданные в последние десятилетия, которые уже стали современной классикой и популярны во всем мире."
            typec = "Современная классика"
            modern = "active"
        case "newepoch":
            desc = "Новые и инновационные коктейли, отражающие современные тенденции в миксологии и технологии приготовления напитков."
            typec = "Напитки новой эры"
            newera = "active"
    
    data, coctailscount, all_pages = FindCategory(typec, 12)
    data_answ = cardformer(data)

    return render(request, "iba.html", {"card": data_answ, "type": typec, "desc": desc,
"count": coctailscount, "pages": pages_block(all_pages, page, "IBA", type), "unforg": unforg, "newera": newera, "modern": modern})

def coctail(request):
    name = request.get_full_path().split("/")[3]
    data = FindName(name)
    if data:
        ingr = ingredients_steps(data)
        steps = CookingSteps(data)

        return render(request, "coctail.html", {"name": data.name, "strength": data.strength, "strength_procent": data.alcohol_percent,
        "time": data.preparation_time, "type": data.type, "image": data.image_url, "history": data.history,
        "ingr_list": ingr, "steps": steps, "glass": data.glass, "temperature": data.serving_temperature})
    else:
        return render(request, "error_page.html")

def contacts(request):
    return render(request, "contacts.html")

def list_coctails(request: HttpRequest):
    page = int(request.get_full_path().split("/")[2][5:])
    try:
        type = request.GET["type"]
        search = request.GET["search"]
    except KeyError:
        type = "all"
        search = ""
    typec = "Все категории"
    match type:
        case "Unforgettable":
            typec = "Незабываемые" 
        case "refreshing":
            typec = "Освежающий"
        case "sweet":
            typec = "Сладкий"
        case "sour":
            typec = "Кислый"
        case "coffee":
            typec = "Кофейный"
        case "non-alcoholic":
            typec = "Безалкогольный"
        case "modern":
            typec = "Современный"
        case "new-epoch":
            typec = "Новой эпохи"
        case "spicy":
            typec = "Пряный"
        case "tropical":
            typec = "Тропический"

    data = searching(type, "none" if not search else search)
    all_pages = len(data)//12

    if len(data) >= 12 and page != all_pages+1:
        data = data[12*page-12:12*page]
    else:
        data = data[12*page-12:len(data)]

    data_answ = cardformer(data)

    return render(request, "list_coctail.html", {"card": data_answ, "pages": pages_block(all_pages, page, search=search, type=type), "search": search, "type": type, "typec": typec})

def admin(request: HttpRequest):
    data = request.POST.dict()

    if len(data) > 1:
        ingr = []
        datalistkey = [*data.keys()]
        datalistvalue = [*data.values()]
        for i in range(len(data)):
            if "ingr" in datalistkey[i]:
                ingr.append(datalistvalue[i], datalistvalue[i+1])
        CreateCoctail(";".join(ingr), *data)

    return render(request, "admin.html")

def error_page(request: HttpRequest):
    return render(request, "error_page.html")