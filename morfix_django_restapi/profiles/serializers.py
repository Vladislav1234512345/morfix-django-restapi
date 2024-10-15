from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404

from .models import Profile, ProfileImage, Hobby, ProfileHobby
from .functions import get_profile

# Сериализатора для хобби
class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('id', 'name')

# Сериализатор для хобби профиля
class ProfileHobbySerializer(serializers.ModelSerializer):  # Используем ModelSerializer
    name = serializers.CharField(max_length=250, required=True)

    class Meta:
        model = ProfileHobby
        fields = ('id', 'name')

    def create(self, validated_data):
        profile = get_profile(self.context.get("request"))
        hobby_name = validated_data['name']

        # Проверяем, существует ли хобби
        try:
            hobby = Hobby.objects.get(name=hobby_name)
        except Hobby.DoesNotExist:
            raise NotFound({"detail": "Данного хобби не существует."})

        # Проверяем, существует ли уже это хобби у профиля
        if ProfileHobby.objects.filter(profile=profile, hobby=hobby).exists():
            raise serializers.ValidationError({"detail": "Данное хобби уже есть."})

        # Создаем новое хобби
        profile_hobby = ProfileHobby.objects.create(profile=profile, hobby=hobby)
        return profile_hobby


# Сериализатор для изображения профиля
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель сериализатора
        model = ProfileImage
        # Поля сериализатора
        fields = ('id', 'image', 'uploaded_at', 'is_main_image')

    # Метод создания объекта profile_image в сериализаторе
    def create(self, validated_data):
        # Получение пользователя из запроса в контексте
        user = self.context['request'].user

        # Получение объекта профиля по параметру user
        profile = get_object_or_404(Profile, user=user)

        profile_image = ProfileImage.objects.create(profile=profile, **validated_data)

        return profile_image



# Сериализатор профиля
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        # Модель сериализатора
        model = Profile
        # Поля сериализатора
        fields = (
            'id',
            'first_name',
            'gender',
            'birthday',
            'dating_purpose',
            'searching_gender',
            'description',
            'smokes_cigarettes',
            'drinks_alcoholics',
            'zodiac_signs',
            'education',
            'job',
            'age',
        )

    # Метод создания экземпляра сериализатора
    def create(self, validated_data):

        # Получение объекта пользователя из запроса в контексте
        user = self.context['request'].user
        # Создаение объекта профиля
        profile = Profile.objects.create(user=user, **validated_data)

        return profile


    # Метод обновления экземпляра сериализатора
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.dating_purpose = validated_data.get('dating_purpose', instance.dating_purpose)
        instance.description = validated_data.get('description', instance.description)
        instance.searching_gender = validated_data.get('searching_gender', instance.searching_gender)
        instance.smokes_cigarettes = validated_data.get('smokes_cigarettes', instance.smokes_cigarettes)
        instance.drinks_alcoholics = validated_data.get('drinks_alcoholics', instance.drinks_alcoholics)
        instance.zodiac_signs = validated_data.get('zodiac_signs', instance.zodiac_signs)
        instance.education = validated_data.get('education', instance.education)
        instance.job = validated_data.get('job', instance.job)
        instance.age = validated_data.get('age', instance.age)

        # Сохраняем изменения профиля
        instance.save()

        return instance