from rest_framework import serializers
from user.models import User, Role, AccessControl, Method
from organization.models import Organization
from feature.apis.serializers import FeatureSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.reverse import reverse


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        role_objects = user.roles.all().values_list("uuid", flat=True)
        roles = [str(role) for role in role_objects]
        token["user_id"] = str(user.uuid)
        token.is_superuser = user.is_superuser
        if user.organization:
            token["organization_id"] = str(user.organization.uuid)
        token["roles"] = roles
        # ...

        return token


class RoleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = Role
        fields = ("id", "name", "display_name", "description")


class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = ("name",)


class AccessControlSerializer(serializers.ModelSerializer):
    feature = serializers.StringRelatedField()
    actions = serializers.StringRelatedField(source="method", many=True)

    class Meta:
        model = AccessControl
        fields = ("feature", "actions")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="users-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization_id = serializers.SlugRelatedField(
        queryset=Organization.objects.all(), slug_field="uuid", source="organization"
    )
    password = serializers.CharField(write_only=True)
    role_ids = serializers.ListField(source="role.uuid", required=False)
    roles = RoleSerializer(read_only=True, many=True)
    organization_url = serializers.HyperlinkedRelatedField(
        source="organization",
        view_name="organizations-detail",
        lookup_field="uuid",
        read_only=True,
    )
    allowed_features = serializers.SerializerMethodField()
    roles_url = serializers.SerializerMethodField()
    features_url = serializers.SerializerMethodField()
    vehicles_url = serializers.SerializerMethodField()
    drivers_url = serializers.SerializerMethodField()
    access_token_url = serializers.SerializerMethodField()
    refresh_token_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "created_at",
            "url",
            "name",
            "address",
            "contact_code",
            "contact_number",
            "email",
            "organization_id",
            "is_active",
            "password",
            "role_ids",
            "roles",
            "organization_url",
            "roles_url",
            "features_url",
            "vehicles_url",
            "drivers_url",
            "access_token_url",
            "refresh_token_url",
            "allowed_features",
        )

    def to_representation(self, user):
        data = super().to_representation(user)
        x = [str(role["id"]) for role in data["roles"]]
        data["role_ids"] = x
        return data

    def create(self, validated_data):
        role_ids = validated_data.pop("role", None)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        if role_ids:
            role_ids = role_ids.pop("uuid")
            roles = Role.objects.filter(uuid__in=role_ids)
            user.roles.add(*roles)
        user.save()
        return user

    def update(self, instance, validated_data):
        role_ids = validated_data.pop("role", None)
        user = super().update(instance=instance, validated_data=validated_data)
        if role_ids:
            role_ids = role_ids.pop("uuid")
            roles = Role.objects.filter(uuid__in=role_ids)
            user.roles.clear()
            user.roles.add(*roles)
        user.save()
        return user

    def get_roles_url(self, user):
        return reverse("roles-list", request=self.context["request"])

    def get_features_url(self, user):
        return reverse("features-list", request=self.context["request"])

    def get_vehicles_url(self, user):
        return reverse("vehicles-list", request=self.context["request"])

    def get_drivers_url(self, user):
        return reverse("drivers-list", request=self.context["request"])

    def get_access_token_url(self, user):
        return reverse("token_obtain_pair", request=self.context["request"])

    def get_refresh_token_url(self, user):
        return reverse("token_refresh", request=self.context["request"])

    def get_allowed_features(self, user):
        # get all roles for that user, and fetch all the access controls for him
        roles = user.roles.all()
        ac = AccessControl.objects.filter(role__in=roles)
        acs = AccessControlSerializer(ac, many=True)
        return acs.data
