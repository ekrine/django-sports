from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (GenerateOtp,
                    VerifyOtp,
                    CreateUser,
                    LoginUser,
                    CreateOpportunity,
                    Follow,
                    GetFollowers)

urlpatterns = {
    url(r'^api/mobile/generateOtp', GenerateOtp.as_view(),name="generateOtp"),
    url(r'^api/mobile/verifyOtp', VerifyOtp.as_view(), name="verifyOtp"),
    url(r'^api/mobile/createUser', CreateUser.as_view(), name="createUser"),
    url(r'^api/mobile/loginUser', LoginUser.as_view(), name="loginUser"),
    url(r'^api/mobile/createOpportunity', CreateOpportunity.as_view(), name="createOpportunity"),
    url(r'^api/mobile/follow', Follow.as_view(), name="follow"),
    url(r'^api/mobile/getFollowers', GetFollowers.as_view(), name="getFollowers"),
}

urlpatterns = format_suffix_patterns(urlpatterns)