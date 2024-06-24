from database.models import Category
from mongoengine.errors import DoesNotExist, ValidationError


class CategoryDAL:
    def get_all_categories(self):
        categories = Category.objects.all()
        categories_dict = []
        for category in categories:
            category_dict = {
                'main_category': category.main_category,
                'sub_category': category.sub_category,
                'id': str(category.id),
            }
            categories_dict.append(category_dict)
        return categories_dict
    
    
    def create_category(self, main_category, sub_category):
        try:
            category = Category(main_category=main_category, sub_category=sub_category)
            category.save()
            return True
        except ValidationError as e:
            raise e
        
    def get_category(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            return {
                'main_category': category.main_category,
                'sub_category': category.sub_category,
                'id': str(category.id)
            }
        except DoesNotExist:
            return None
        
    def update_category(self, category_id, main_category=None, sub_category=None):
        try:
            category = Category.objects.get(id=category_id)
            if main_category:
                category.main_category = main_category
            if sub_category:
                category.sub_category = sub_category
            category.save()
            return category.to_dict()
        except DoesNotExist:
            return None
        except ValidationError as e:
            raise e

    def delete_category(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return True
        except DoesNotExist:
            return False