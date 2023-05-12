from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class ReviewsCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "kyu@mail.com", "password":"123","nickname":"nick"}
        cls.review_data = {"title":"kyu title","content":"내요오오옹","movie_code":222222}
        cls.user = User.objects.create_user("kyu@mail.com","123","nick")

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    def test_fail_if_not_logged_in(self):
        url = reverse("review_list")
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, 401)

    def test_create_review(self):
        response = self.client.post(
            path=reverse("review_list"),
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["message"], "작성완료")
        self.assertEqual(response.status_code, 200)

class ReviewReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.reviews = []
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(),cls.faker.word(),cls.faker.name())
            cls.reviews.append(Review.objects.create(title=cls.faker.sentence(),content=cls.faker.text(),user=cls.user))

    def test_get_review(self):
        for review in self.reviews:
            url = review.get_absolute_url()
            response = self.client.get(url)
            serializer = ReviewSerializer(review).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)