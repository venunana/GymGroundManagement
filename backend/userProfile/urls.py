from django.urls import path
from .views import (
    UserCreateView,
    UserProfileDetailView,
    UserLoginView,
    UserProfileUpdateView,
    UserListView,
    GetStudentUsersView,
    UserTypeUpdateView,
    UserRegisterView,
    UserProfileCreateView,
    CreateAcademicStaffUserView,
    CreatePostgraduateUserView,
    CreateUniversityStudentUserView,
    ProvinceListView,
    CityListView,
    UserDeleteView,
    TotalUserCountView,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("register2/", UserRegisterView.as_view(), name="register2"),
    path("register/profile/", UserProfileCreateView.as_view(), name="register-profile"),
    path(
        "register/profile/academic/",
        CreateAcademicStaffUserView.as_view(),
        name="academic",
    ),
    path(
        "register/profile/postgraduate/",
        CreatePostgraduateUserView.as_view(),
        name="postgraduate",
    ),
    path(
        "register/profile/student/",
        CreateUniversityStudentUserView.as_view(),
        name="student",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileDetailView.as_view(), name="profile"),
    path("profile/update/", UserProfileUpdateView.as_view(), name="profile-update"),
    path("student-users/", GetStudentUsersView.as_view(), name="student-users"),
    path("profile/all-profiles/", UserListView.as_view(), name="all-profiles"),
    path(
        "profile/<int:pk>/update-user-type/",
        UserTypeUpdateView.as_view(),
        name="profile-type-update",
    ),
    path("provinces/", ProvinceListView.as_view(), name="provinces"),
    path("cities/", CityListView.as_view(), name="cities"),
    path("profile/delete/", UserDeleteView.as_view(), name="profile-delete"),
    path("total-users/", TotalUserCountView.as_view(), name="total-users"),
]
