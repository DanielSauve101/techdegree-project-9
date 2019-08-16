from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ItemForm, MenuForm
from .models import Menu, Item, Ingredient
from .views import (menu_list, menu_detail, create_new_menu, edit_menu,
                    item_list, item_detail, create_new_item, edit_item)

class Setup_Class(TestCase):
    def setUp(self):
        #Created a fake user for the chef
        self.user = User.objects.create_user(
            username='daniel', email='dan@hotmail.com', password='top_secret')

        #Creates ingredients to add to items
        self.apple = Ingredient.objects.create(name='apple')
        self.orange = Ingredient.objects.create(name='orange')
        self.kiwi = Ingredient.objects.create(name='kiwi')

        #Created an item to use in the menu
        self.fruitbowl = Item.objects.create(
            name='fruitbowl',
            description='Bowl of fresh cut assorted fruits',
            created_date='2019-01-01 12:00:00Z',
            chef=self.user,
            standard='True'
        )
        self.fruitbowl.ingredients.add(self.apple)
        self.fruitbowl.ingredients.add(self.orange)
        self.fruitbowl.ingredients.add(self.kiwi)

        #Created menu
        self.menu = Menu.objects.create(
            season='Winter 2021',
            created_date='2019-01-02 12:00:00Z',
            expiration_date='2019-12-31 12:00:00Z'
        )
        self.menu.items.add(self.fruitbowl)

class MenuViewsTests(Setup_Class):
    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
                                        kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, 'fruitbowl')

    def test_valid_create_new_menu_view(self):
        menu_count = Menu.objects.count()
        form_data = {
            'season': "summer 2022",
            'items': ['1'],
            'created_date': "2019-1-1",
            'expiration_date': "2019-12-12"
            }
        resp = self.client.post('/menu/new/', data=form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Menu.objects.count(), menu_count+1)

    def test_blank_create_new_menu_view(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_form.html')
        
    def test_edit_menu(self):
        resp = self.client.get(reverse('menu_edit',
                                        kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_form.html')

    def test_item_list(self):
        resp = self.client.get(reverse('item_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')

    def test_valid_item_detail(self):
        resp = self.client.get(reverse('item_detail',
                                        kwargs={'pk': self.fruitbowl.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
        self.assertContains(resp, self.apple)

    def test_invalid_item_detail(self):
        resp = self.client.get(reverse('item_detail',
                                        kwargs={'pk': '2'}))
        self.assertEqual(resp.status_code, 404)

    def test_blank_create_new_item_view(self):
        resp = self.client.get(reverse('item_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_form.html')

    def test_edit_item_view(self):
        resp = self.client.get(reverse('item_edit',
                                        kwargs={'pk': self.fruitbowl.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_form.html')


class MenuFormTests(Setup_Class):
    def test_menuform_invalidform(self):
        form_data = {
            'season': "asdf",
            'items': ['1'],
            'created_date': "2019-1-1",
            'expiration_date': "2019-12-12"
            }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_menuform_validform(self):
        form_data = {
            'season': "winter 123",
            'items': ['1'],
            'created_date': "2019-1-1",
            'expiration_date': "2019-12-12"
            }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())
