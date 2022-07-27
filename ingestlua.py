###########################
#  WORK ON LUA INGESTION  #
#   will move elsewhere   #
###########################


from slpp import slpp as lua
import json

# open recipe.lua and assign to var f
with open('recipe.lua', 'r') as f:
    # convert to string
    f = ('').join(f)
    # decode lua and save to var data
    data = lua.decode(f[13:-2])


"""

Prototype of recipe object per recipe

{
    NAME: {
        'name': NAME,
        'ingredients': {
            ING1: AMOUNT1,
            ING2: AMOUNT2,
        },
        'ingredients_exp': { ### if "expensive" key in object
            ING1: AMOUNT1,
            ING2: AMOUNT2,
        },
        'results': {
            RESULT1: AMOUNT1, ### amount from "result_count" or 1
            RESULT2: AMOUNT2,
        }
        'energy_used': ENERGY, ### "energy_required"
        'factory_type': FACTORY, ### "category", translated via dictionary
        'icon': ICON ### "icon" or "icons/{NAME}.png" (move /fluid/ to parent???)
    },
    ...
}


"""

data = json.dumps(data, sort_keys=True, indent=4)
data = json.loads(data)
for recipe in data:
    print(recipe['name'])
    if 'ingredients' in recipe:
        temp_ingredients = recipe['ingredients']
    else:
        # need to add expensive ingredients
        temp_ingredients = recipe['normal']['ingredients']
        print('boop')
    recipe['ingredients'] = {}
    for ingredient in temp_ingredients:
        if type(ingredient) == list:
            recipe['ingredients'][ingredient[0]] = ingredient[1]
        elif type(ingredient) == dict:
            recipe['ingredients'][ingredient['name']] = ingredient['amount']

data = json.dumps(data, sort_keys=True, indent=4)

with open('recipes.json', 'w') as f:
    f.write(data)
