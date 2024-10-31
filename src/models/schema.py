class Schema:
    def __init__(self, native_class, classes):
        self.native_class = native_class
        self.classes = classes

    def __repr__(self):
        return f"Schema(native_class={self.native_class}, classes={self.classes})"
    
class Item_Schema:
    def __init__(self, class_name, display_name, form):
        self.class_name = class_name
        self.display_name = display_name
        self.form = form

    def __repr__(self):
        return f"Item_Schema(class_name={self.class_name}, display_name={self.display_name}, form={self.form})"
    
class Recipe_Schema:
    def __init__(self, class_name, display_name, ingredients, products, produced_in, manufactoring_duration):
        self.class_name = class_name
        self.display_name = display_name
        self.ingredients = ingredients
        self.products = products
        self.produced_in = produced_in
        self.manufactoring_duration = manufactoring_duration

    def __repr__(self):
        return (f"Recipe_Schema(class_name={self.class_name}, display_name={self.display_name}, "
                f"ingredients={self.ingredients}, products={self.products}, "
                f"produced_in={self.produced_in}, manufactoring_duration={self.manufactoring_duration})")

class Recipe:
    def __init__(self, recipe_name, base_item, input_1, input_1_per_min, input_2, input_2_per_min, input_3, input_3_per_min, input_4, input_4_per_min, output_1, output_1_per_min, output_2, output_2_per_min, building):
        self.recipe_name = recipe_name
        self.base_item = base_item
        self.input_1 = input_1
        self.input_1_per_min = input_1_per_min
        self.input_2 = input_2
        self.input_2_per_min = input_2_per_min
        self.input_3 = input_3
        self.input_3_per_min = input_3_per_min
        self.input_4 = input_4
        self.input_4_per_min = input_4_per_min
        self.output_1 = output_1
        self.output_1_per_min = output_1_per_min
        self.output_2 = output_2
        self.output_2_per_min = output_2_per_min
        self.building = building

    def __repr__(self):
        return (f"Recipe(recipe_name={self.recipe_name}, base_item={self.base_item}, "
                f"input_1={self.input_1}, input_1_per_min={self.input_1_per_min}, "
                f"input_2={self.input_2}, input_2_per_min={self.input_2_per_min}, "
                f"input_3={self.input_3}, input_3_per_min={self.input_3_per_min}, "
                f"input_4={self.input_4}, input_4_per_min={self.input_4_per_min}, "
                f"output_1={self.output_1}, output_1_per_min={self.output_1_per_min}, "
                f"output_2={self.output_2}, output_2_per_min={self.output_2_per_min}, "
                f"building={self.building})")