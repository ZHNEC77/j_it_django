from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
# Create your tests here.


class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_data = {'title': 'Test Task',
                          'description': 'This is a test task'}
        self.response = self.client.post(
            '/api/tasks/', self.task_data, format='json')

    def test_create_task(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_get_task_list(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_task_detail(self):
        task = Task.objects.get()
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        task = Task.objects.get()
        updated_data = {'title': 'Updated Task',
                        'description': 'This is a update test task', 'completed': True}
        response = self.client.put(
            f'/api/tasks/{task.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'Updated Task')
        self.assertEqual(Task.objects.get().description,
                         'This is a update test task')
        self.assertEqual(Task.objects.get().completed, True)

    def test_partial_update_task(self):
        task = Task.objects.get()
        updated_data = {'title': 'Partially Updated Task'}
        response = self.client.patch(
            f'/api/tasks/{task.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'Partially Updated Task')

    def test_delete_task(self):
        task = Task.objects.get()
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_get_nonexistent_task(self):
        response = self.client.get('/api/tasks/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_task(self):
        updated_data = {'title': 'Updated Task', 'completed': True}
        response = self.client.put(
            '/api/tasks/999999/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_nonexistent_task(self):
        updated_data = {'title': 'Partially Updated Task'}
        response = self.client.patch(
            '/api/tasks/999999/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_task(self):
        response = self.client.delete('/api/tasks/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
