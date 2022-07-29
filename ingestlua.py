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


factory_lookup = {
    'oil-processing': 'oil-refinery',
    'crafting-with-fluid': 'ass', ########temp name
    'chemistry': 'chem', ########temp name
    'crafting': 'ass', ########temp name
    'rocket-building': 'rocket', ########temp name
    'centrifuging': 'cent', ########temp name
    'advanced-crafting': 'ass', ########temp name
    'smelting': 'miner', ########temp name

}


items_dict = {}

for recipe in data:
    items_dict[recipe['name']] = {
        'name': recipe['name'],
        'energy_used': recipe['energy_required'] if 'energy_required' in recipe else 'WTF', ########temp need to figure out actual value
        'results': recipe['result'] if 'result' in recipe else recipe['results'] if 'results' in recipe else 'WTF', #this isn't right - handle multiple better
        'factory_type': factory_lookup[recipe['category']] if 'category' in recipe else 'ass', ########temp name
        'icon': 'ADD ICONS', ########temp 
        
    }


    # print(recipe['name'])
    if 'ingredients' in recipe:
        temp_ingredients = recipe['ingredients']
    else:
        # need to add expensive ingredients
        temp_ingredients = recipe['normal']['ingredients']
        temp_ingredients_exp = recipe['expensive']['ingredients']
        print('boop')
    recipe['ingredients'] = {}
    for ingredient in temp_ingredients:
        if type(ingredient) == list:
            recipe['ingredients'][ingredient[0]] = ingredient[1]
        elif type(ingredient) == dict:
            recipe['ingredients'][ingredient['name']] = ingredient['amount']
    


print(items_dict)


# data = json.dumps(items_dict, sort_keys=True, indent=4)
data = json.dumps(data, sort_keys=True, indent=4)

with open('recipes.json', 'w') as f:
    f.write(data)
