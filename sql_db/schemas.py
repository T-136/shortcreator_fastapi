from pydantic import BaseModel, Field


# class Clip(BaseModel):
#     clip_id: int = Field(example = 1)
#     gMapsLink: str | None = Field(default=None, example = "https://www.google.de/maps/@48.8612317,2.3580157,3a,90y,252.82h,111.54t/data=!3m8!1e1!3m6!1sAF1QipOgCOtwlsGA-uBiAwpBQPuC7PzlD1UrB-4S7zGc!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipOgCOtwlsGA-uBiAwpBQPuC7PzlD1UrB-4S7zGc%3Dw203-h100-k-no-pi-17.66881-ya160.10611-ro0-fo100!7i13312!8i6656")
#     name: str | None = Field(default=None, example="ein Stein")
#     group: str | None = Field(default=None, example="ein Stein")
#     videotext: str | None = Field(default=None, example="ein Stein")
#     latlong: str | None = Field(default=None, example="ein Stein")
#     start: int | None = Field(default=None, example=1)
#     stop: int | None = Field(default=None, example=10)
#     isRenderd: bool | None = Field(default=None, example=False)
#     isUploadedYt: bool | None = Field(default=None, example=False)
#     isUploadedTikTok: bool | None = Field(default=None, example=False)
#     isUploadedInstagram: bool | None = Field(default=None, example=False)
#     streetviewVideo = bytes | None 

#     class config:
#         orm = True

# class Ymusic(BaseModel):
#     ymusic_id: str
#     title:  str

# class ClipBase(BaseModel):
#     clipd_id: int


# class ClipCreate(Clip):
#     pass