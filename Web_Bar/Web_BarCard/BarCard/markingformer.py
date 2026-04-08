from .services import Cocktail

def cardformer(data: list[Cocktail]) -> str:
    data_answ = ""
    for i in data:
        ingr = ''
        for n in i.ingredients:
            ingr += n.name + " "
        data_answ += \
        f"""
        <a href="http://127.0.0.1:8000/list/coctail/{i.name}/">
            <article class="cocktail-card">
            <img src="{i.image_url}" alt="{i.name}" class="cocktail-img">
            <div class="cocktail-info">
                <div class="cocktail-header">
                    <h3 class="cocktail-name">{i.name}</h3>
                    <span class="cocktail-badge">{i.type}</span>
                </div>
                <span class="cocktail-category">{i.category}</span>
                <p class="cocktail-desc">{i.description}</p>
                <p class="cocktail-ingredients"><strong>Основа:</strong>{ingr}</p>
                <div class="cocktail-footer">
                    <div class="cocktail-glass">
                        <i class="fas fa-glass-whiskey"></i>{i.glass}
                    </div>
                    <div class="cocktail-strength">
                        <i class="fas fa-tachometer-alt"></i>{i.strength}
                    </div>
                </div>
            </article>
        </a>"""
    return data_answ

def pages_block(count, page, where="list", type='', search='') -> str:
    answ = ''
    for i in range(1 if page-3 != 1 else page-3, page+3 if count+2 >= page+3 else count+2):

        answ += \
        f"""<a href="http://127.0.0.1:8000/{where}/page-{i}/?type={type}&search={search}">
            <div class="block-page">
                <p class="no-select">{i}</p>
            </div>
        </a>"""
    return answ

def CookingSteps(data: Cocktail) -> str:
    steps = ''
    for m in data.recipe_steps:
        steps += f"""
    <li class="step-item">
        <p class="step-text">{m[m.find(".")+1:]}</p>
    </li>
    """
    return steps
            
def ingredients_steps(data: Cocktail):
    ingr = ''
    for i in data.ingredients:
        ingr += f"""
    <li class="ingredient-item">
        <div class="ingredient-name">
            <i class="fas fa-wine-bottle"></i> {i.name}
        </div>
        <span class="ingredient-amount">{i.volume}</span>
    </li>
    """
    return ingr