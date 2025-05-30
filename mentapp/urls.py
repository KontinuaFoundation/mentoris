from django.urls import path

from .views import VolumeChapterView, VolumesView

urlpatterns = [
    path("<int:volume_number>/", VolumeChapterView.as_view(), name="volume_chapter"),
    path("", VolumesView.as_view(), name="volumes")
]

