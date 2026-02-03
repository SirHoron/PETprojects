from django.shortcuts import render

def main(request):
    name, category, desc, ingr, scr = "","","","","",
    topcoctail = f"""
    <a href="http://127.0.0.1:8000/list/coctail/{id}">
        <article class="cocktail-card">
            <img src="{scr}" alt="{name}" class="cocktail-img">
            <div class="cocktail-info">
                <h3 class="cocktail-name">{name}</h3>
                <span class="cocktail-category">{category}</span>
                <p class="cocktail-desc">{desc}</p>
                <p class="cocktail-ingredients"><strong>Основа:</strong>{ingr}</p>
            </div>
        </article>
    </a>"""
    return render(request, "main.html")

def IBA(request):
    return render(request, "IBA.html")

def coctail(request):
    return render(request, "coctail.html")

def contacts(request):
    return render(request, "contacts.html")

def list_coctails(request):
    return render(request, "list_coctail.html")