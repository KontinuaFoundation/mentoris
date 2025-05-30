from django.shortcuts import render
from django.views import View

# Create your views here.
from mentapp.models import Chapter_Loc, Volume, Chapter

class VolumeChapterView(View):
    def get(self, request, volume_number):
        volume = Volume.objects.get(number=volume_number)
        chapters = Chapter.objects.filter(volume=volume)
        chapters_loc = Chapter_Loc.objects.filter(chapter__in=chapters).order_by('chapter')
        return render(request, 'mentapp/volume.html', {'volume': volume, 'chapters': chapters_loc})

class VolumesView(View):
    def get(self, request):
        volumes = Volume.objects.filter()
        return render(request, 'mentapp/landing.html', {'volumes': volumes})