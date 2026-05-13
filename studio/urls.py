from django.contrib import admin
from django.urls import path
from studio.views import audio_segments, avatar_videos, class_segments, classes, exercises, views


urlpatterns = [
    path("admin/dashboard", views.studio_admin_dashboard, name="studio-admin-dashboard"),
    path("admin/profile", views.studio_admin_profile, name="studio-admin-profile"),
    
    
    # classes
    path("classes", classes.index, name="classes-index"),
    path("classes/list", classes.ClassesListView.as_view(), name="classes-list"),
    path("classes/create", classes.create, name="classes-create"),
    path("classes/edit/<uuid:uuid>", classes.edit, name="classes-edit"),
    path("classes/view/<uuid:uuid>", classes.view, name="classes-view"),
    path("classes/delete/<uuid:uuid>", classes.delete, name="classes-delete"),
    
    
    # exercises
    path("exercises", exercises.index, name="exercises-index"),
    path("exercises/list", exercises.ExercisesListView.as_view(), name="exercises-list"),
    path("exercises/create", exercises.create, name="exercises-create"),
    path("exercises/edit/<uuid:uuid>", exercises.edit, name="exercises-edit"),
    path("exercises/view/<uuid:uuid>", exercises.view, name="exercises-view"),
    path("exercises/delete/<uuid:uuid>", exercises.delete, name="exercises-delete"),
    
    
    path("class-segments", class_segments.index, name="class-segments-index"),
    path("class-segments/list", class_segments.ClassSegmentsListView.as_view(), name="class-segments-list" ),
    path("class-segments/create", class_segments.create, name="class-segments-create"),
    path("class-segments/edit/<uuid:uuid>", class_segments.edit, name="class-segments-edit"),
    path("class-segments/view/<uuid:uuid>",class_segments.view, name="class-segments-view"),
    path("class-segments/delete/<uuid:uuid>", class_segments.delete, name="class-segments-delete"),
    
    # audio segments
    path("audio-segments", audio_segments.index, name="audio-segments-index"),
    path("audio-segments/list", audio_segments.AudioSegmentsListView.as_view(), name="audio-segments-list"),
    path("audio-segments/create", audio_segments.create, name="audio-segments-create"),
    path("audio-segments/edit/<uuid:uuid>", audio_segments.edit, name="audio-segments-edit"),
    path("audio-segments/view/<uuid:uuid>", audio_segments.view, name="audio-segments-view"),
    path("audio-segments/delete/<uuid:uuid>", audio_segments.delete, name="audio-segments-delete"),
    
    # avatar vidoes
    path("avatar-videos", avatar_videos.index, name="avatar-videos-index"),
    path("avatar-videos/list", avatar_videos.AvatarVideosListView.as_view(), name="avatar-videos-list"),
    path("avatar-videos/create", avatar_videos.create, name="avatar-videos-create"),
    path("avatar-videos/edit/<uuid:uuid>", avatar_videos.edit, name="avatar-videos-edit"),
    path("avatar-videos/view/<uuid:uuid>", avatar_videos.view, name="avatar-videos-view"),
    path("avatar-videos/delete/<uuid:uuid>", avatar_videos.delete, name="avatar-videos-delete"),
]
