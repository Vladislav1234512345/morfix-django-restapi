import profile

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Profile, ProfileImage

# Сериализатор для изображения профиля
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель сериализатора
        model = ProfileImage
        # Поля сериализатора
        fields = ('id', 'image', 'is_main_image')

    # Метод создания объекта profile_image в сериализаторе
    def create(self, validated_data):
        # Получение пользователя из запроса в контексте
        user = self.context['request'].user
        # profile = Profile.objects.get(user=user)

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
            'last_name',
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
        )

        # Поля сериализатора только для чтения
        read_only_fields = ('age',)

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
        instance.last_name = validated_data.get('last_name', instance.last_name)
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

        # Сохраняем изменения профиля
        instance.save()

        return instance