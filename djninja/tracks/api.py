from email import message
from typing import List, Optional
from ninja import NinjaAPI, File 
from ninja.files import UploadedFile
from typing import List
from requests import request
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema
api = NinjaAPI()


@api.get("/tracks", response=List[TrackSchema])
def tracks(request, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()


@api.get("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {"message": "Track you are looking for does not exist!"}

@api.post("/tracks", response={201: TrackSchema})
def create_track(request, track: TrackSchema):
    track = Track.objects.create(**track.dict())
    return track


@api.put("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def change_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {"message": "Track you are looking for does not exist!"}


