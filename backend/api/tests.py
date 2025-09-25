from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note
from .serializers import NoteSerializer, UserSerializer
import json


class NoteModelTestCase(TestCase):
    """Sample test cases for somethings and some others"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.note = Note.objects.create(
            title='Test Note',
            content='This is a test note content',
            author=self.user
        )
    
    def test_note_creation(self):
        """Test note creation"""
        self.assertEqual(self.note.title, 'Test Note')
        self.assertEqual(self.note.content, 'This is a test note content')
        self.assertEqual(self.note.author, self.user)
        self.assertIsNotNone(self.note.created_at)
    
    def test_note_str_method(self):
        self.assertEqual(str(self.note), 'Test Note')
    
    def test_note_author_relationship(self):
        """Test the relationship between Note and User"""
        self.assertEqual(self.user.notes.count(), 1)
        self.assertEqual(self.user.notes.first(), self.note)
    
    def test_note_fields_max_length(self):
        """Test of field constraints"""
        long_title = 'A' * 101 
        note = Note(title=long_title, content='Test content', author=self.user)
        
        with self.assertRaises(Exception):
            note.full_clean()


class NoteSerializerTestCase(TestCase):
    """Test cases for Note serializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.note = Note.objects.create(
            title='Test Note',
            content='Test content',
            author=self.user
        )
    
    def test_note_serialization(self):
        """Test note serialization"""
        serializer = NoteSerializer(self.note)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Test Note')
        self.assertEqual(data['content'], 'Test content')
        self.assertEqual(data['author_username'], 'testuser')
        self.assertEqual(data['author_id'], self.user.id)
        self.assertIn('created_at', data)
    
    def test_note_deserialization(self):
        """Test note deserialization"""
        data = {
            'title': 'New Note',
            'content': 'New content'
        }
        serializer = NoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class UserSerializerTestCase(TestCase):
    """Test cases for the User serializer"""
    
    def test_user_creation(self):
        """Test user for creation through serializer"""
        data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('newpass123'))
    
    def test_password_write_only(self):
        """Test if the password is write-only"""
        user = User.objects.create_user(username='testuser', password='testpass')
        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)


class NoteAPITestCase(APITestCase):
    """Test cases for Note API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Test notes
        self.note1 = Note.objects.create(
            title='Note 1',
            content='Content 1',
            author=self.user
        )
        
        self.note2 = Note.objects.create(
            title='Note 2',
            content='Content 2',
            author=self.admin_user
        )
    
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_list_notes_authenticated(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('note-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see all notes
    
    def test_list_notes_unauthenticated(self):
        url = reverse('note-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_note_authenticated(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': 'New note content'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3)
        
        new_note = Note.objects.latest('created_at')
        self.assertEqual(new_note.title, 'New Note')
        self.assertEqual(new_note.author, self.user)
    
    def test_create_note_unauthenticated(self):
        """Test if is posible to create a note when not auth"""
        url = reverse('note-list')
        data = {
            'title': 'New Note',
            'content': 'New note content'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_note_invalid_data(self):
        """Test if is posible to create a note with invalid data"""
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('note-list')
        data = {
            'title': '',  # the '' should fail
            'content': 'Content'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_note_as_admin(self):
        """Deleting a note as admin user"""
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('delete-note', kwargs={'pk': self.note1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.filter(pk=self.note1.pk).count(), 0)
    
    def test_delete_note_as_regular_user(self):
        """Deleting a note as regular user"""
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('delete-note', kwargs={'pk': self.note1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Note.objects.filter(pk=self.note1.pk).count(), 1)
    
    def test_delete_nonexistent_note(self):
        """Deleting a unexisting (is it spell like that?) note"""
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('delete-note', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CurrentUserAPITestCase(APITestCase):
    """Test cases for CurrentUser API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
    
    def get_jwt_token(self, user):
        """Helper method to get JWT token for a user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_current_user_regular(self):
        """Getting current user info for regular user"""
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        
        self.assertEqual(data['username'], 'testuser')
        self.assertFalse(data['is_admin'])
        self.assertFalse(data['is_staff'])
        self.assertFalse(data['is_superuser'])
    
    def test_current_user_admin(self):
        """Getting current user info for admin user"""
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        
        self.assertEqual(data['username'], 'admin')
        self.assertTrue(data['is_admin'])
        self.assertTrue(data['is_staff'])
        self.assertTrue(data['is_superuser'])
    
    def test_current_user_unauthenticated(self):
        """Getting current user info when not authenticated"""
        url = reverse('current-user')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRegistrationAPITestCase(APITestCase):
    """Test cases for User registration API"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration_success(self):
        """Test if the user registration is successful"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_registration_duplicate_username(self):
        """Registration with duplicate username"""
        # Create an already existing (it is spell like that) user
        User.objects.create_user(username='existinguser', password='pass123')
        
        url = reverse('register')
        data = {
            'username': 'existinguser',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_invalid_data(self):
        """Registration with invalid data"""
        url = reverse('register')
        data = {
            'username': '',  
            'password': 'pass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)