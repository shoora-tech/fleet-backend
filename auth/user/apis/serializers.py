from rest_framework import serializers
from user.models import User, Role
from organization.models import Organization
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
        fields = ("id", "name", "description")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="users-detail", lookup_field="uuid", lookup_url_kwarg="uuid"
    )
    organization_id = serializers.SlugRelatedField(
        queryset=Organization.objects.all(), slug_field="uuid", source="organization"
    )
    password = serializers.CharField(write_only=True, required=True)
    role_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    roles = RoleSerializer(read_only=True, many=True)
    organization_url = serializers.HyperlinkedRelatedField(
        source="organization",
        # queryset = Organization.objects.all(),
        view_name="organizations-detail",
        lookup_field="uuid",
        read_only=True,
    )
    roles_url = serializers.SerializerMethodField()
    features_url = serializers.SerializerMethodField()
    vehicles_url = serializers.SerializerMethodField()
    drivers_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
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
        )

    def create(self, validated_data):
        role_ids = validated_data.pop("role_ids", None)
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        if role_ids:
            roles = Role.objects.filter(uuid__in=role_ids)
            user.roles.add(*roles)
        user.save()
        return user

    def get_roles_url(self, org):
        return reverse("roles-list", request=self.context["request"])

    def get_features_url(self, org):
        return reverse("features-list", request=self.context["request"])

    def get_vehicles_url(self, org):
        return reverse("vehicles-list", request=self.context["request"])

    def get_drivers_url(self, org):
        return reverse("drivers-list", request=self.context["request"])
