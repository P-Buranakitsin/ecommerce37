from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from app.forms import UserRegisterForm, UserProfileForm
from app.models import Type, Commodities, CartItem, Purchase, UserProfile
from app.views import ProfileView


# Create your tests here.

class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for all tests in this class
        bag_type = Type.objects.create(name='Bag')
        clothing_type = Type.objects.create(name='Clothing')
        fruit_type = Type.objects.create(name='Fruit')

        Commodities.objects.create(c_name='Bag1', price=99, type=bag_type)
        Commodities.objects.create(c_name='Bag2', price=199, type=bag_type)
        Commodities.objects.create(c_name='Clothing1', price=99, type=clothing_type)
        Commodities.objects.create(c_name='Fruit1', price=9.9, type=fruit_type)

    def test_location(self):
        # test view url exists at desired location
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_name(self):
        # test view url accessible by name and correct template
        response = self.client.get(reverse('app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/home.html')

    def test_popularCommodities(self):
        # test context contains popular commodities
        response = self.client.get(reverse('app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('most_popular_items' in response.context)
        popular_items = response.context['most_popular_items']
        self.assertTrue(popular_items.filter(type__name='Bag').count() == 2)

    def test_otherCommodities(self):
        # test context contains other commodities
        response = self.client.get(reverse('app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('other_items' in response.context)
        other_items = response.context['other_items']
        self.assertTrue(other_items.filter(type__name='Clothing').count() == 1)
        self.assertTrue(other_items.filter(type__name='Fruit').count() == 1)


class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_type = Type.objects.create(name='Test_type')
        for i in range(20):
            Commodities.objects.create(c_name=f'Test_Item_{i}',
                                       price=10,
                                       description="Test_description",
                                       type=test_type
                                       )

    def test_location(self):
        # test view url exists at desired location
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_name(self):
        # test view url accessible by name
        response = self.client.get(reverse('app:search'))
        self.assertEqual(response.status_code, 200)

    def test_correctTemplate(self):
        # test view uses correct template
        response = self.client.get(reverse('app:search'))
        self.assertTemplateUsed(response, 'app/search.html')

    def test_emptyQuery(self):
        # test view with empty query
        response = self.client.get(reverse('app:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test_Item_0")
        self.assertContains(response, "Test_Item_8")

    def test_query(self):
        # test view with query
        response = self.client.get(reverse('app:search') + '?item_name=test_item_5')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test_Item_5")
        self.assertNotContains(response, "Test_Item_0")
        self.assertNotContains(response, "Test_Item_19")



class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('app:login')
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_login_success(self):
        # test login success
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('app:home'))
        self.assertTrue(authenticate(username='test_user', password='test_password'))

    def test_login_failure(self):
        # test login failure
        data = {'username': 'test_user', 'password': 'wrong_password'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(authenticate(username='test_user', password='wrong_pass'))



class UserRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('app:register')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')
        self.assertIsInstance(response.context['user_form'], UserRegisterForm)
        self.assertIsInstance(response.context['profile_form'], UserProfileForm)

    def test_post_request(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:home'))

        user = User.objects.get(username=data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password1']))
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])


class CommodityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_type = Type.objects.create(name='Test_type')
        cls.commodity = Commodities.objects.create(
            c_name='Test Commodity',
            price=10.99,
            description='This is a test commodity',
            type=test_type,
        )

    def test_location(self):
        # test view url exists at desired location
        response = self.client.get(f'/commodity/{self.commodity.c_id}/')
        self.assertEqual(response.status_code, 200)

    def test_correctTemplate(self):
        # test view uses correct template
        response = self.client.get(f'/commodity/{self.commodity.c_id}/')
        self.assertTemplateUsed(response, 'app/commodity.html')

    def test_selectedItem(self):
        # test view context contains selected item
        response = self.client.get(f'/commodity/{self.commodity.c_id}/')
        self.assertEqual(response.context['selected_item'], self.commodity)

    def test_relatedItems(self):
        # test view context contains related item
        response = self.client.get(f'/commodity/{self.commodity.c_id}/')
        self.assertTrue('related_items' in response.context)


class ContactUsViewTest(TestCase):
    def test_location(self):
        # test view url exists at desired location
        response = self.client.get('/contactUs/')
        self.assertEqual(response.status_code, 200)

    def test_correctTemplate(self):
        # test view uses correct template
        response = self.client.get('/contactUs/')
        self.assertTemplateUsed(response, 'app/contactUs.html')


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.cart_item = CartItem.objects.create(user=self.user, commodities=self.commodities, amount=2)

    def test_cart_view_with_login(self):
        # test cart view with login
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('app:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/cart.html')
        self.assertEqual(len(response.context['cart_items']), 1)
        self.assertEqual(response.context['total_price'], 20)

    def test_cart_view_without_login(self):
        # test cart view without login
        response = self.client.get(reverse('app:cart'))
        self.assertRedirects(response, reverse('app:login') + '?next=' + reverse('app:cart'))


class AddtoCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.url = reverse('app:add_to_cart')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_authenticated_user(self):
        # authenticated user
        self.client.force_login(self.user)
        data = {'c_id': self.commodities.c_id, 'amount': 2}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'authenticated': True, 'total_items': 2})

    def test_post_unauthenticated_user(self):
        # unauthenticated user
        data = {'c_id': self.commodities.c_id, 'amount': 2}
        #response = self.client.post(self.url, data=data)
        response = self.client.post(self.url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.json(), {'authenticated': False})


class RemoveFromCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.cart_item = CartItem.objects.create(user=self.user, commodities=self.commodities, amount=2)
        self.url = reverse('app:remove_from_cart')

    def test_removeItem(self):
        # test remove item (post)
        self.client.force_login(self.user)
        data = {'itemID': self.commodities.c_id}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_removeAllItems(self):
        # test remove all items (post)
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

class UpdateCartViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.cart_item = CartItem.objects.create(user=self.user, commodities=self.commodities, amount=2)
        self.url = reverse('app:update_cart')

    def test_post_updateCart(self):
        self.client.force_login(self.user)
        #data = {'cart_items': '[{"itemId": %d, "amount": 3}]' % self.commodities.c_id}
        data = {'cart_items': '[{"itemId": %d, "quantity": 3}]' % self.commodities.c_id}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.get().amount, 3)


class CheckoutCartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.cart_item = CartItem.objects.create(user=self.user, commodities=self.commodities, amount=2)
        self.url = reverse('app:checkout_cart')

    def test_checkoutCartView(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)

'''
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user',
            password='test_pass',
        )
        test_type = Type.objects.create(name='Test_type')
        self.commodities = Commodities.objects.create(c_name='Test Commodity',
                                                      price=10,
                                                      description='Test Description',
                                                      type=test_type,
                                                      )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.purchase = Purchase.objects.create(user=self.user, commodities=self.commodities, amount=2)

    def test_get(self):
        # Test with a valid user
        #response = self.client.get(reverse('app:profile', args=['testuser']))
        request = self.factory.get(reverse_lazy('app:profile', kwargs={'username': self.user.username}))
        response = ProfileView.as_view()(request, username=self.user.username)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(request, 'app/profile.html')
        #self.assertIn('items_page', request.context)
        #self.assertIn('user_profile', request.context)
        #self.assertIn('selected_user', request.context)
        self.assertIn('form', request.context)

        # Test with an invalid user
        response = self.client.get(reverse('app:profile', args=['invaliduser']))
        self.assertRedirects(response, reverse('app:index'))

    def test_post(self):
        # Test with valid form data
        self.client.login(username='test_user', password='test_pass')
        data = {'old_password': 'test_pass', 'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(reverse('app:profile', args=['test_user']), data)
        self.assertRedirects(response, reverse('app:home'))

        # Test with invalid form data
        data = {'old_password': 'test_pass', 'new_password1': 'new_pass123', 'new_password2': 'invalidpass'}
        response = self.client.post(reverse('app:profile', args=['test_user']), data)
        self.assertEqual(response.status_code, 200)
'''

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', email='test@123.com', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_get_userDetails(self):
        # test get user's details
        view = ProfileView()
        user, user_profile, form = view.get_user_details(self.user.username)
        self.assertEqual(user, self.user)
        self.assertEqual(user_profile, self.user_profile)
        self.assertIsNotNone(form)

    def test_get(self):
        request = self.factory.get(reverse_lazy('app:profile', kwargs={'username': self.user.username}))
        request.user = self.user
        response = ProfileView.as_view()(request, username=self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        # Test with valid form data
        '''
        data = {'old_password': 'password123', 'new_password1': 'newpassword456', 'new_password2': 'newpassword456'}
        print(self.user.username)
        request = self.factory.post(reverse_lazy('app:profile', kwargs={'username': self.user.username}), data)
        request.user = self.user
        response = ProfileView.as_view()(request, username=self.user.username)
        #print(response.content)
        self.assertEqual(response.status_code, 302)
        #self.assertRedirects(response, reverse_lazy('app:home'))
        self.assertRedirects(response, reverse('app:home'))
        '''
        self.client.login(username='test_user', password='password123')
        data = {'old_password': 'password123', 'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(reverse('app:profile', args=['test_user']), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:home'))

    def test_post_invalid(self):
        # Test with invalid form data
        request = self.factory.post(reverse_lazy('app:profile', kwargs={'username': self.user.username}), {'new_password1': 'new_password', 'new_password2': 'wrong_password'})
        request.user = self.user
        response = ProfileView.as_view()(request, username=self.user.username)
        self.assertEqual(response.status_code, 200)


class UploadProfileImageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.url = reverse('app:upload_profile_image')

    def test_upload_valid_image(self):
        # Log in the user
        self.client.login(username='test_user', password='test_password')

        # Create an image object
        image = Image.new('RGB', (100, 100), color='red')
        image.save('test_image.png')

        # Upload the image
        with open('test_image.png', 'rb') as f:
            response = self.client.post(reverse('app:upload_profile_image'), {'picture': f})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the image is saved to the user's profile
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.userprofile.picture)

        # Clean up
        self.user.userprofile.picture.delete()

    def test_upload_no_image(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 302)
