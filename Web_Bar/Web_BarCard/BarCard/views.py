from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import For_Card_Coctail

""" 
CardCoctail( name=, category=, type=, ingredients=, description=, glass=, strength=, image=, badge= )
"""

""" Дополнительные функции """

def pages_block(count, page):
    answ = ''
    for i in range(1 if page-3 != 1 else page-3, page+3 if count+2 >= page+3 else count+2):
        answ += \
        f"""<a href="http://127.0.0.1:8000/list/page-{i}/">
            <div class="block-page">
                <p class="no-select">{i}</p>
            </div>
        </a>"""
    return answ

def card_form(data):
    data_answ = ""
    for i in data:
        i = i.__dict__
        answ = ingredients_handler(i["ingredients"].split("/"))
        data_answ += \
        f"""
        <a href="http://127.0.0.1:8000/list/coctail/{i["name"]}/">
            <article class="cocktail-card">
            <img src="" alt="{i['name']}" class="cocktail-img">
            <div class="cocktail-info">
                <div class="cocktail-header">
                    <h3 class="cocktail-name">{i['name']}</h3>
                    <span class="cocktail-badge">{i['type']}</span>
                </div>
                <span class="cocktail-category">{i["category"]}</span>
                <p class="cocktail-desc">{i['description']}</p>
                <p class="cocktail-ingredients"><strong>Основа:</strong>{answ}</p>
                <div class="cocktail-footer">
                    <div class="cocktail-glass">
                        <i class="fas fa-glass-whiskey"></i>{i['glass']}
                    </div>
                    <div class="cocktail-strength">
                        <i class="fas fa-tachometer-alt"></i>{i['strength']}
                    </div>
                </div>
            </article>
        </a>"""
    return data_answ

def ingredients_handler(ingr):
    answ = ""
    for m in range(len(ingr)):
        ingr[m] = ingr[m].split(".")
    for n in range(len(ingr)):
        answ += f" {ingr[n][0]}"
    return answ


"""  Страницы  """
def main(request):
    data = For_Card_Coctail.objects.all()
    if len(data) >= 6:
        data = data[:6]
    else:
        data = data[:len(data)]

    data_answ = card_form(data)

    return render(request, "main.html", {"coctails": data_answ})

def IBA(request: HttpRequest):
    page = int(request.get_full_path().split("/")[2][5:])
    desc = ''
    unforg = ''
    newera = ''
    modern = ''
    typec = ''
    try:
        type = request.GET["type"]
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
    except KeyError:
        return render(request, "error_page.html")
    
    data = For_Card_Coctail.objects.filter(category=type)
    all_pages = len(data)//12
    coctailscount = len(data)
    if len(data) >= 12 and page != all_pages+1:
        data = data[12*page-12:12*page]
    else:
        data = data[12*page-12:len(data)]
    data_answ = card_form(data)

    return render(request, "IBA.html", {"card": data_answ, "type": typec, "desc": desc,
"count": coctailscount, "pages": pages_block(all_pages, page), "unforg": unforg, "newera": newera, "modern": modern})

def coctail(request):
    ingr = ''
    steps = ''
    name = request.get_full_path().split("/")[3]
    print(name)
    data = For_Card_Coctail.objects.get(name=name).__dict__
    ingredi = data["ingredients"].split("/")
    for i in ingredi[:len(ingredi)-1]:
        i = i.split(".")
        print(i)
        ingr += f"""
    <li class="ingredient-item">
        <div class="ingredient-name">
            <i class="fas fa-wine-bottle"></i> {i[0]}
        </div>
        <span class="ingredient-amount">{i[1]} мл</span>
    </li>
    """
    
    data_step = data["cooking"].split(":")
    if len(data_step) > 1:
        run_steps = data_step[0]
        for m in data_step[1].split(";"):
            steps += f"""
        <li class="step-item">
            <p class="step-text">{m}.</p>
        </li>
        """
    else:
        run_steps = data_step[0]
    return render(request, "coctail.html", {"name": data["name"], "strength": data["strength"], "strength_procent": data["strengthprocent"],
    "time": f"{data["ctime"]}-{int(data["ctime"])+1}", "type": data["type"], "image": data["image"], "history": data["history"],
    "ingr_list": ingr, "run_steps": run_steps, "steps": steps, "glass": data["glass"], "temperature": f"{data["temperature"]}-{int(data["temperature"])+3}"})

def contacts(request):
    return render(request, "contacts.html")

def list_coctails(request: HttpRequest):
    page = int(request.get_full_path().split("/")[2][5:])

    data = For_Card_Coctail.objects.all()
    all_pages = len(data)//12
    if len(data) >= 12 and page != all_pages+1:
        data = data[12*page-12:12*page]
    else:
        data = data[12*page-12:len(data)]

    data_answ = card_form(data)

    return render(request, "list_coctail.html", {"card": data_answ, "pages": pages_block(all_pages, page)})

def admin(request: HttpRequest):
    data = request.POST.dict()

    if len(data) > 1:
        ingr = ""
        datalistkey = [*data.keys()]
        datalistvalue = [*data.values()]
        for i in range(len(data)):
            if "ingr" in datalistkey[i]:
                ingr += datalistvalue[i] + "." +datalistvalue[i+1] + "/"
        For_Card_Coctail.objects.create(name=data["name"], category=data["category"], type=data["type"], ingredients=ingr,\
        description=data["description"], glass=data["glass"], strength=data["strenght"], image=data["image"], temperature=data["tmre"], ctime=data["ctime"],\
        history=data["history"], cooking=data["cooking"], strengthprocent=data["strengthprocent"],)

    return render(request, "admin.html")

def error_page(request: HttpRequest):
    return render(request, "error_page.html")