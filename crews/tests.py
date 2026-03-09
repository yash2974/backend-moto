from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from crews.models import Crew, Request
from users.models import Profile


class CrewModelTestCase(TestCase):
    """Test cases for Crew model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.user)
    
    def test_create_crew(self):
        """Test creating a crew"""
        crew = Crew.objects.create(
            name='Test Crew',
            description='Test Description',
            type='Sports',
            owner=self.user,
            is_private='Public'
        )
        self.assertEqual(crew.name, 'Test Crew')
        self.assertEqual(crew.owner, self.user)
        self.assertEqual(crew.is_private, 'Public')
    
    def test_crew_string_representation(self):
        """Test crew __str__ method"""
        crew = Crew.objects.create(name='Thunder Riders', owner=self.user)
        self.assertEqual(str(crew), 'Thunder Riders')


class CrewCreateAPITestCase(APITestCase):
    """Test cases for creating crews"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        Profile.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_public_crew(self):
        """Test creating a public crew"""
        data = {
            'name': 'Public Riders',
            'description': 'A public crew',
            'type': 'Sports',
            'is_private': 'Public',
            'country': 'USA',
            'city': 'New York'
        }
        response = self.client.post('/api/my-crews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Public Riders')
        
        # Verify owner is automatically added as member
        crew = Crew.objects.get(name='Public Riders')
        self.assertIn(self.user, crew.members.all())
    
    def test_create_invite_only_crew(self):
        """Test creating an invite only crew"""
        data = {
            'name': 'Invite Only Crew',
            'type': 'Adventure',
            'is_private': 'Invite Only'
        }
        response = self.client.post('/api/my-crews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_private'], 'Invite Only')
    
    def test_create_crew_without_auth(self):
        """Test creating a crew without authentication"""
        self.client.force_authenticate(user=None)
        data = {'name': 'Test Crew'}
        response = self.client.post('/api/my-crews/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_crew_duplicate_name(self):
        """Test creating a crew with duplicate name"""
        Crew.objects.create(name='Unique Crew', owner=self.user)
        data = {'name': 'Unique Crew'}
        response = self.client.post('/api/my-crews/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CrewJoinAPITestCase(APITestCase):
    """Test cases for joining crews"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='memberpass123'
        )
        Profile.objects.create(user=self.owner)
        Profile.objects.create(user=self.member)
        
        self.public_crew = Crew.objects.create(
            name='Public Crew',
            owner=self.owner,
            is_private='Public'
        )
        self.public_crew.members.add(self.owner)
        
        self.invite_only_crew = Crew.objects.create(
            name='Invite Only Crew',
            owner=self.owner,
            is_private='Invite Only'
        )
        self.invite_only_crew.members.add(self.owner)
        
        self.client = APIClient()
    
    def test_join_public_crew(self):
        """Test joining a public crew - should join immediately"""
        self.client.force_authenticate(user=self.member)
        response = self.client.post(f'/api/crews/{self.public_crew.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Joined crew')
        
        # Verify member was added
        self.public_crew.refresh_from_db()
        self.assertIn(self.member, self.public_crew.members.all())
    
    def test_join_invite_only_crew(self):
        """Test joining an invite only crew - should create a request"""
        self.client.force_authenticate(user=self.member)
        response = self.client.post(f'/api/crews/{self.invite_only_crew.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Request sent')
        
        # Verify request was created
        request_obj = Request.objects.get(user=self.member, crew=self.invite_only_crew)
        self.assertEqual(request_obj.status, 'pending')
        
        # Verify member was NOT added yet
        self.invite_only_crew.refresh_from_db()
        self.assertNotIn(self.member, self.invite_only_crew.members.all())
    
    def test_join_already_member(self):
        """Test joining a crew when already a member"""
        self.public_crew.members.add(self.member)
        self.client.force_authenticate(user=self.member)
        response = self.client.post(f'/api/crews/{self.public_crew.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Already a member')
    
    def test_join_as_owner(self):
        """Test owner trying to join their own crew"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(f'/api/crews/{self.public_crew.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Already a member')
    
    def test_join_request_duplicate(self):
        """Test sending duplicate join request"""
        self.client.force_authenticate(user=self.member)
        
        # First request
        self.client.post(f'/api/crews/{self.invite_only_crew.id}/join/')
        
        # Second request (duplicate)
        response = self.client.post(f'/api/crews/{self.invite_only_crew.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Request already sent')


class CrewLeaveAPITestCase(APITestCase):
    """Test cases for leaving crews"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='memberpass123'
        )
        Profile.objects.create(user=self.owner)
        Profile.objects.create(user=self.member)
        
        self.crew = Crew.objects.create(
            name='Test Crew',
            owner=self.owner,
            is_private='Public'
        )
        self.crew.members.add(self.owner, self.member)
        
        self.client = APIClient()
    
    def test_leave_crew(self):
        """Test leaving a crew"""
        self.client.force_authenticate(user=self.member)
        response = self.client.post(f'/api/crews/{self.crew.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Left crew')
        
        # Verify member was removed
        self.crew.refresh_from_db()
        self.assertNotIn(self.member, self.crew.members.all())
    
    def test_owner_cannot_leave(self):
        """Test that owner cannot leave their own crew"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(f'/api/crews/{self.crew.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Owner cannot leave crew')
    
    def test_leave_when_not_member(self):
        """Test leaving a crew when not a member"""
        non_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@example.com',
            password='password123'
        )
        Profile.objects.create(user=non_member)
        
        self.client.force_authenticate(user=non_member)
        response = self.client.post(f'/api/crews/{self.crew.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Not a member')


class CrewRequestManagementTestCase(APITestCase):
    """Test cases for managing join requests (approve/reject)"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='memberpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='password123'
        )
        Profile.objects.create(user=self.owner)
        Profile.objects.create(user=self.member)
        Profile.objects.create(user=self.other_user)
        
        self.crew = Crew.objects.create(
            name='Test Crew',
            owner=self.owner,
            is_private='Invite Only'
        )
        self.crew.members.add(self.owner)
        
        self.join_request = Request.objects.create(
            user=self.member,
            crew=self.crew,
            status='pending'
        )
        
        self.client = APIClient()
    
    def test_get_pending_requests(self):
        """Test getting pending requests for a crew"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f'/api/my-crews/{self.crew.id}/requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], 'member')
        self.assertEqual(response.data[0]['status'], 'pending')
    
    def test_approve_request(self):
        """Test approving a join request"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f'/api/my-crews/{self.crew.id}/requests/{self.join_request.id}/approve/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Request approved')
        
        # Verify request status updated
        self.join_request.refresh_from_db()
        self.assertEqual(self.join_request.status, 'approved')
        
        # Verify member was added to crew
        self.crew.refresh_from_db()
        self.assertIn(self.member, self.crew.members.all())
    
    def test_reject_request(self):
        """Test rejecting a join request"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f'/api/my-crews/{self.crew.id}/requests/{self.join_request.id}/reject/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Request rejected')
        
        # Verify request status updated
        self.join_request.refresh_from_db()
        self.assertEqual(self.join_request.status, 'rejected')
        
        # Verify member was NOT added to crew
        self.crew.refresh_from_db()
        self.assertNotIn(self.member, self.crew.members.all())
    
    def test_process_already_processed_request(self):
        """Test processing a request that was already processed"""
        self.join_request.status = 'approved'
        self.join_request.save()
        
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f'/api/my-crews/{self.crew.id}/requests/{self.join_request.id}/approve/'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Request already processed')
    
    def test_process_nonexistent_request(self):
        """Test processing a request that doesn't exist"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f'/api/my-crews/{self.crew.id}/requests/99999/approve/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Request not found')
    
    def test_non_owner_cannot_process_request(self):
        """Test that non-owner cannot approve/reject requests"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(
            f'/api/my-crews/{self.crew.id}/requests/{self.join_request.id}/approve/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CrewListAPITestCase(APITestCase):
    """Test cases for listing crews"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)
        
        # Public crew
        self.public_crew = Crew.objects.create(
            name='Public Crew',
            owner=self.user1,
            is_private='Public'
        )
        self.public_crew.members.add(self.user1)
        
        # Invite Only crew
        self.invite_crew = Crew.objects.create(
            name='Invite Only Crew',
            owner=self.user1,
            is_private='Invite Only'
        )
        self.invite_crew.members.add(self.user1)
        
        self.client = APIClient()
    
    def test_list_crews_authenticated(self):
        """Test listing crews as authenticated user"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/crews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # User2 should see Public and Invite Only crews
        crew_names = [crew['name'] for crew in response.data]
        self.assertIn('Public Crew', crew_names)
        self.assertIn('Invite Only Crew', crew_names)
    
    def test_list_my_crews(self):
        """Test listing only owned crews"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/my-crews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_crews_unauthenticated(self):
        """Test listing crews without authentication"""
        response = self.client.get('/api/crews/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
