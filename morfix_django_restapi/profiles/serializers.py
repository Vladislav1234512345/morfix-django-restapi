import profile

from rest_framework import serializers
from .models import Profile, ProfileImage

# Сериализатор для изображения профиля
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель сериализатора
        model = ProfileImage
        # Поля сериализатора
        fields = ('image', 'is_profile_image')

# Сериализатор профиля
class ProfileSerializer(serializers.ModelSerializer):
    # Вызов сериализатора "ProfileImageSerializer"
    # параметр many означает, что сериализатор "ProfileImageSerializer" принимает список изображений
    # параметр required=True означает, что сериализатор требует изображения
    images = ProfileImageSerializer(many=True, required=True)

    class Meta:
        # Модель сериализатора
        model = Profile
        # Поля сериализатора
        fields = (
            'first_name',
            'last_name',
            'gender',
            'birthday',
            'dating_purpose',
            'description',
            'searching_gender',
            'smokes_cigarettes',
            'drinks_alcoholics',
            'zodiac_signs',
            'education',
            'job',
            'images',
        )

        # Поля сериализатора только для чтения
        read_only_fields = ('age',)

    # Функция создания экземпляра сериализатора
    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        profile = Profile.objects.create(**validated_data)

        for image_data in images_data:
            ProfileImage.objects.create(profile=profile, **image_data)

        return profile

    # Функция обновления экземпляра сериализатора
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
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

        for image_data in images_data:
            ProfileImage.objects.update_or_create(profile=profile, **image_data)

        return instance