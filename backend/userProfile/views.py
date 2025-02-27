from django.conf import settings
from urllib.parse import urlencode
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from sport.models import Sport

from rest_framework import views, generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from backend.utils import generate_unique_identifier, get_profile_picture_path
from .permissions import IsAdminUserType

from .serializers import (
    UserDataSerializer,
    UserSerializer,
    UserProfileSerializer,
    ProvinceSerializer,
    CitySerializer,
    AuthSerializer,
    UserTypeUpdateSerializer,
    AcademicStaffSerializer,
    PostgraduateUserSerializer,
    UniversityStudentUserSerializer,
    LoginSerializer,
)
from .models import (
    UserProfile,
    UserType,
    AcademicStaffUser,
    PostgraduateUser,
    UniversityStudentUser,
    Province,
    City,
    Faculty,
)

from member.models import Members

from .services import get_user_data


# --------------------------------Creation Views--------------------------------
# -------------UserCreateView-------------
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(f"Serializer: {serializer}")
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        profile = UserProfile.objects.get(user=serializer.instance)
        profile_serializer = UserProfileSerializer(profile)

        response_data = {
            "status": "success",
            "message": "User created successfully.",
            "data": {
                **serializer.data,
                **profile_serializer.data,
            },
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


# -------------UserRegisterView-------------
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = request.data
        # print(user_data)
        serializer = self.get_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        unique_identifier = generate_unique_identifier()
        cache.set(unique_identifier, user, timeout=5500)

        return_resp = {
            "status": "success",
            "message": "User info saved successfully.",
            "identifier": unique_identifier,
            "data": serializer.data,
        }

        return JsonResponse(
            return_resp,
            status=status.HTTP_200_OK,
        )


# -------------UserProfileCreateView-------------
class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        identifier = request.data.get("identifier")
        user_data = cache.get(identifier)
        # print("\n\nUser Data: ", user_data.email)
        if not user_data:
            return Response(
                {"error": "Invalid or expired identifier."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_data.save()

        user = User.objects.get(email=user_data.email)

        request.data["user"] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return_resp = {
            "status": "success",
            "message": "UserProfile created successfully.",
            "data": serializer.data,
        }

        return JsonResponse(
            return_resp,
            status=status.HTTP_201_CREATED,
        )


# -------------CreateAcademicStaffUserView-------------
class CreateAcademicStaffUserView(generics.CreateAPIView):
    queryset = AcademicStaffUser.objects.all()
    serializer_class = AcademicStaffSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Copy the request data
        user = request.user  # Get the logged-in user

        # Ensure the user is authenticated
        if user.is_anonymous:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Add the logged-in user to the data
        data["user"] = user.id

        # Initialize the serializer with the modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save the academic staff user
        academic_staff_user = serializer.save()

        return_resp = {
            "status": "success",
            "message": "Academic Staff User Info Added Successfully",
            "data": serializer.data,
        }

        return JsonResponse(
            return_resp,
            status=status.HTTP_200_OK,
        )


# -------------CreatePostgraduateUserView-------------
class CreatePostgraduateUserView(generics.CreateAPIView):
    queryset = PostgraduateUser.objects.all()
    serializer_class = PostgraduateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Copy the request data
        user = request.user  # Get the logged-in user

        # Ensure the user is authenticated
        if user.is_anonymous:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Add the logged-in user to the data
        data["user"] = user.id

        # Initialize the serializer with the modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        postgraduate_user = serializer.save()

        return_resp = {
            "status": "success",
            "message": "Postgraduate User Info Added Successfully",
            "data": serializer.data,
        }

        return JsonResponse(
            return_resp,
            status=status.HTTP_200_OK,
        )


# -------------CreateUniversityStudentUserView-------------
class CreateUniversityStudentUserView(generics.CreateAPIView):
    queryset = UniversityStudentUser.objects.all()
    serializer_class = UniversityStudentUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Copy the request data
        user = request.user  # Get the logged-in user

        # Ensure the user is authenticated
        if user.is_anonymous:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Add the logged-in user to the data
        data["user"] = user.id

        # Initialize the serializer with the modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        university_student_user = serializer.save()

        return_resp = {
            "status": "success",
            "message": "University Student User Info Added Successfully",
            "data": serializer.data,
        }

        return JsonResponse(
            return_resp,
            status=status.HTTP_200_OK,
        )


# --------------------------------User Authentication Views--------------------------------
# -------------GoogleLoginApi-------------
class GoogleLoginApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data

        try:
            user_data = get_user_data(validated_data)
        except Exception as e:
            params = urlencode({"error": e})
            redirect_url = f"{settings.BASE_APP_URL}/login?{params}"

            return redirect(redirect_url)

        user = User.objects.get(email=user_data["email"])
        group = Group.objects.get(name="internal")
        user.groups.add(group)
        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        redirect_url = f"{settings.BASE_APP_URL}/loading?access_token={access_token}&refresh_token={refresh_token}"

        return redirect(redirect_url)


# -------------UserLoginView-------------
class UserLoginView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            try:
                membership = Members.objects.get(user=user)
                is_member = True
            except Members.DoesNotExist:
                is_member = False
            refresh = RefreshToken.for_user(user)
            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            try:
                user_profile = UserProfile.objects.get(user=user)
                profile_picture = get_profile_picture_path(user_profile)

                profile_data = {
                    "national_id": user_profile.national_id,
                    "contact": user_profile.contact,
                    "profile_picture": profile_picture,
                    "user_type": user_profile.user_type.name,
                    "city": user_profile.city.label,
                    "address": user_profile.address,
                    "date_of_birth": user_profile.date_of_birth,
                    "is_member": is_member,
                }
            except UserProfile.DoesNotExist:
                profile_data = {}

            return_resp = {
                "status": "success",
                "message": "User logged in successfully.",
                "data": {
                    "user": user_data,
                    "profile": profile_data,
                },
                "auth_tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }

            return JsonResponse(return_resp, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------User Profile Views--------------------------------
# -------------UserProfileDetailView-------------
class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        if self.kwargs.get("pk") is None:
            user = self.request.user

            try:
                profile = UserProfile.objects.get(user=user)
                return profile
            except UserProfile.DoesNotExist:
                raise NotFound("User Profile not found")
        else:
            user = self.request.user
            profile = UserProfile.objects.get(user=user)
            user_id = self.kwargs.get("pk")

            try:
                if profile.user_type.name == "admin":
                    profile = UserProfile.objects.get(pk=user_id)
                    return profile
                else:
                    raise PermissionDenied(
                        "You do not have permission to perform this action."
                    )
            except UserProfile.DoesNotExist:
                raise NotFound("User Profile not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        profile_picture_url = get_profile_picture_path(instance)
        user = instance.user
        user_type = instance.user_type

        try:
            membership = Members.objects.get(user=user)
            is_member = True
        except Members.DoesNotExist:
            is_member = False

        user_type_data = {}
        if user_type.name == "student":
            student_profile = UniversityStudentUser.objects.get(user=user)
            user_type_data = {
                "registration_number": student_profile.registration_number,
                "faculty": student_profile.faculty.name,
            }
        elif user_type.name == "academic":
            academic_staff_profile = AcademicStaffUser.objects.get(user=user)
            user_type_data = {
                "upf_number": academic_staff_profile.upf_number,
                "faculty": academic_staff_profile.faculty.name,
                "date_of_appointment": academic_staff_profile.date_of_appointment,
            }
        elif user_type.name == "postgraduate":
            postgraduate_profile = PostgraduateUser.objects.get(user=user)
            user_type_data = {
                "pg_registration_number": postgraduate_profile.pg_registration_number,
                "pg_commencement_date": postgraduate_profile.pg_commencement_date,
            }

        user_data = {
            "user": {
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
                "email": instance.user.email,
                "username": instance.user.username,
            },
            "profile": {
                "id": instance.user.id,
                "national_id": (
                    instance.national_id if instance.national_id else "Not Provided"
                ),
                "profile_picture": profile_picture_url,
                "contact": instance.contact if instance.contact else "Not Provided",
                "user_type": instance.user_type.name,
                "date_of_birth": (
                    instance.date_of_birth if instance.date_of_birth else ""
                ),
                "city": instance.city.label if instance.city else "Not Provided",
                "province": (
                    instance.city.province.label if instance.city else "Not Provided"
                ),
                "is_member": is_member,
            },
            "user_type_data": user_type_data,
        }
        response_data = {
            "status": "success",
            "message": "User profile retrieved successfully.",
            "data": user_data,
        }
        # print(response_data)
        return JsonResponse(response_data, status=status.HTTP_200_OK)


# -------------UserListView-------------
class UserListView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not request.user.groups.filter(name="admin").exists():
            return Response(
                {
                    "status": "error",
                    "message": "You do not have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "message": "All profiles retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# -------------StudentUserListView-------------
class GetStudentUsersView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.filter(user_type__name="student").select_related(
                "user"
            )
        else:
            return UserProfile.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if (
            not request.user.groups.filter(name="admin").exists()
            and not request.user.groups.filter(name="staff").exists()
        ):
            return Response(
                {
                    "status": "error",
                    "message": "You do not have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            student_profiles = serializer.data
            resp_data = self.customize_response_data(student_profiles)
            return self.get_paginated_response(resp_data)

        serializer = self.get_serializer(queryset, many=True)
        student_profiles = serializer.data
        resp_data = self.customize_response_data(student_profiles)
        return Response(
            {
                "status": "success",
                "message": "All student profiles retrieved successfully.",
                "data": resp_data,
            },
            status=status.HTTP_200_OK,
        )

    def customize_response_data(self, data):
        resp_data = []
        for student in data:
            try:
                user_profile = UserProfile.objects.select_related("user").get(
                    id=student["id"]
                )
                university_student = UniversityStudentUser.objects.select_related(
                    "faculty"
                ).get(user=user_profile.user)
                profile_picture_url = (
                    user_profile.profile_picture.url
                    if user_profile.profile_picture
                    else None
                )
                resp_data.append(
                    {
                        "id": user_profile.user_id,
                        "first_name": user_profile.user.first_name,
                        "last_name": user_profile.user.last_name,
                        "profile_picture": profile_picture_url,
                        "reg_number": university_student.registration_number,
                        "faculty": university_student.faculty.name,
                    }
                )
            except ObjectDoesNotExist as e:
                # Handle the case where related objects do not exist
                print(f"Error: {e}")
        return resp_data


# --------------------------------Update Views--------------------------------
# -------------UserProfileUpdateView-------------
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            return profile
        except UserProfile.DoesNotExist:
            raise NotFound("User Profile not found")

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "User profile updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# -------------UserTypeUpdateView-------------
class UserTypeUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserTypeUpdateSerializer
    permission_classes = [IsAdminUserType]

    def update(self, request, *args, **kwargs):
        user_profile_id = self.kwargs.get("pk")

        try:
            user_profile = UserProfile.objects.get(pk=user_profile_id)
        except UserProfile.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "User Profile not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user_type = serializer.validated_data["user_type"]
            user_type_name = user_type.name
            group = Group.objects.get(name=user_type_name)

            try:
                if user_profile.user_type.name == "staff" and user_type_name != "staff":
                    Sport.objects.filter(in_charge=user_profile.user).update(
                        in_charge=None
                    )

                user_profile.user_type = user_type
                user_profile.save()
                user_profile.user.groups.add(group)

                resp_data = {
                    "user": user_profile.user.email,
                    "user_type": user_type_name,  # Convert to string representation
                }

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "User type updated",
                        "data": resp_data,
                    },
                    status=status.HTTP_200_OK,
                )
            except UserType.DoesNotExist:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "UserType does not exist",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# -------------ProvinceListView-------------
class ProvinceListView(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return JsonResponse(
            {
                "status": "success",
                "message": "Provinces retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# -------------CityListView-------------
class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return JsonResponse(
            {
                "status": "success",
                "message": "Cities retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# -------------UserDeleteView-------------
class UserDeleteView(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            return profile
        except UserProfile.DoesNotExist:
            raise NotFound("User Profile not found")

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user

        # Delete the user profile and the user
        profile.delete()
        user.delete()

        return JsonResponse(
            {
                "status": "success",
                "message": "User and associated data deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )


class TotalUserCountView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        if (
            not request.user.groups.filter(name="admin").exists()
            and not request.user.groups.filter(name="staff").exists()
        ):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "You do not have permission to perform this action.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        user_count = User.objects.count()
        return JsonResponse(
            {
                "status": "success",
                "message": "Total user count retrieved successfully.",
                "data": user_count,
            },
            status=status.HTTP_200_OK,
        )
