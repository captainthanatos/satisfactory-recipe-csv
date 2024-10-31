import json
import csv
from models.schema import Schema, Item_Schema, Recipe_Schema, Recipe

valid_buildings = ["Constructor", "Assembler", "Manufacturer", "Smelter", "Foundry", "Blender", "Converter", "Refinery", "Packager", "HadronCollider", "QuantumEncoder"]

def read_file(file_path):
    with open(file_path, "r", encoding="utf-16") as file:
        data = json.load(file)
        return data
    
def create_schema_list(data):
    schema_list = []
    for data_dictionary in data:
        native_class = data_dictionary.get("NativeClass")
        classes = data_dictionary.get("Classes")
        schema = Schema(native_class, classes)
        schema_list.append(schema)
    return schema_list

def create_item_schema_list(classes):
    item_list = []
    for class_dictionary in classes:
        class_name = class_dictionary.get("ClassName")
        display_name = class_dictionary.get("mDisplayName")
        form = class_dictionary.get("mForm")
        if class_name and display_name:
            item = Item_Schema(class_name, display_name, form)
            item_list.append(item)
    return item_list

def create_and_filter_recipe_schema_list(classes):
    recipe_schema_list = []
    for class_dictionary in classes:
        class_name = class_dictionary.get("ClassName")
        display_name = class_dictionary.get("mDisplayName")
        ingredients = class_dictionary.get("mIngredients")
        products = class_dictionary.get("mProduct")
        manufactoring_duration = class_dictionary.get("mManufactoringDuration")
        produced_in = class_dictionary.get("mProducedIn")
        
        if class_name and display_name and ingredients and products and manufactoring_duration and produced_in:
            if contains_valid_building(produced_in):
                recipe_schema = Recipe_Schema(class_name, display_name, ingredients, products, produced_in, manufactoring_duration)
                recipe_schema_list.append(recipe_schema)
    return recipe_schema_list

def contains_valid_building(string):
    return any(building in string for building in valid_buildings)

def process_recipes(recipe_schemas, item_schemas):
    recipe_list = []
    for recipe_schema in recipe_schemas:
        recipe_name = recipe_schema.display_name
        inputs = split_and_remove_parenthesis(recipe_schema.ingredients)
        outputs = split_and_remove_parenthesis(recipe_schema.products)
        base_item = get_item_name(item_schemas, outputs[0])

        input_1 = get_item_name(item_schemas, inputs[0])
        input_1_per_min = get_item_per_min(inputs[1], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, input_1))
        input_2 = get_item_name(item_schemas, inputs[2]) if len(inputs) > 2 else None
        input_2_per_min = get_item_per_min(inputs[3], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, input_2)) if len(inputs) > 3 else 0
        input_3 = get_item_name(item_schemas, inputs[4]) if len(inputs) > 4 else None
        input_3_per_min = get_item_per_min(inputs[5], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, input_3)) if len(inputs) > 5 else 0
        input_4 = get_item_name(item_schemas, inputs[6]) if len(inputs) > 6 else None
        input_4_per_min = get_item_per_min(inputs[7], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, input_4)) if len(inputs) > 7 else 0
        
        output_1 = get_item_name(item_schemas, outputs[0])
        output_1_per_min = get_item_per_min(outputs[1], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, output_1))
        output_2 = get_item_name(item_schemas, outputs[2]) if len(outputs) > 2 else None
        output_2_per_min = get_item_per_min(outputs[3], recipe_schema.manufactoring_duration, is_gas_or_liquid(item_schemas, output_2)) if len(outputs) > 3 else 0
        
        building = get_building_name(recipe_schema.produced_in)
        
        recipe = Recipe(recipe_name, base_item, input_1, input_1_per_min, input_2, input_2_per_min, input_3, input_3_per_min, input_4, input_4_per_min, output_1, output_1_per_min, output_2, output_2_per_min, building)
        recipe_list.append(recipe)
    return recipe_list
        
def split_and_remove_parenthesis(string):
    if not string:
        return []
    items = string.split(",")
    return [item.replace("(", "").replace(")", "").strip() for item in items]

def get_item_name(item_schemas, class_name):
    for item in item_schemas:
        if item.class_name in class_name:
            return item.display_name

def is_gas_or_liquid(item_schemas, display_name):
    for item in item_schemas:
        if item.display_name == display_name:
            return "GAS" in item.form or "LIQUID" in item.form
    return False
    
def get_item_per_min(amount, duration, is_gas_or_liquid):
    duration = float(duration)
    if is_gas_or_liquid:
        amount = float(get_amount(amount)) / 1000
    else:
        amount = float(get_amount(amount))
    return (60/duration) * amount

def get_amount(string):
    return string.split("=")[1]

def get_building_name(string):
    for building in valid_buildings:
        if building in string:
            return building
        
def sort_recipes_by_base_item(recipes):
    filtered_recipes = [recipe for recipe in recipes if recipe.base_item is not None]
    return sorted(filtered_recipes, key=lambda recipe: recipe.base_item)

def recipes_to_csv(recipes, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Recipe Name", "Base Item", "Input 1", "Input 1 Per Min", "Input 2", "Input 2 Per Min",
            "Input 3", "Input 3 Per Min", "Input 4", "Input 4 Per Min", "Output 1", "Output 1 Per Min",
            "Output 2", "Output 2 Per Min", "Building"
        ])
        for recipe in recipes:
            writer.writerow([
                recipe.recipe_name, recipe.base_item, recipe.input_1, recipe.input_1_per_min,
                recipe.input_2, recipe.input_2_per_min, recipe.input_3, recipe.input_3_per_min,
                recipe.input_4, recipe.input_4_per_min, recipe.output_1, recipe.output_1_per_min,
                recipe.output_2, recipe.output_2_per_min, recipe.building
            ])

if __name__ == "__main__":
    data = read_file('../content/en-US.json')
    schemas = create_schema_list(data)
    item_schemas = create_item_schema_list(schemas[0].classes)
    item_schemas.extend(create_item_schema_list(schemas[12].classes))
    item_schemas.extend(create_item_schema_list(schemas[14].classes))
    item_schemas.extend(create_item_schema_list(schemas[15].classes))
    item_schemas.extend(create_item_schema_list(schemas[16].classes))
    item_schemas.extend(create_item_schema_list(schemas[17].classes))
    item_schemas.extend(create_item_schema_list(schemas[19].classes))
    item_schemas.extend(create_item_schema_list(schemas[23].classes))
    item_schemas.extend(create_item_schema_list(schemas[26].classes))
    item_schemas.extend(create_item_schema_list(schemas[75].classes))
    recipe_schemas = create_and_filter_recipe_schema_list(schemas[6].classes)
    recipes = process_recipes(recipe_schemas, item_schemas)
    recipes = sort_recipes_by_base_item(recipes)
    # for index, schema in enumerate(schemas):
    #     if 'powershard' in schema.native_class.lower():
    #         print(f"Index: {index}, Schema: {schema.native_class}")
    recipes_to_csv(recipes, '../content/recipes_output.csv')
    print("Done!")
