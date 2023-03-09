from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import os
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
import cv2
from .forms import FileUploadForm
from .models import CustomFile

@login_required(login_url="auth/login")
def getFiles(req):
    form = FileUploadForm()
    files = CustomFile.objects.filter(author=req.user)
    totalUsed = sum([file.size for file in files])
    totalAllowed = 104857600
    remaining = totalAllowed - totalUsed
    return render(
        req,
        template_name="storage/home.html",
        context={
            "form": form,
            "files": files,
            "totalUsed": totalUsed,
            "remaining": remaining,
            "totalAllowed": totalAllowed,
        },
    )


@login_required(login_url="auth/login")
def uploadFile(req,remaining_size):
    if req.method == "POST":
        form = FileUploadForm(req.POST, req.FILES)
        if form.is_valid():
            fileData = req.FILES["file"]
            if fileData.size > int(remaining_size):
                messages.error(req, 'File size more than the remaining quota. Please choose a file within the size limit or remove some old files.')
                return redirect("/")    
            file = CustomFile.objects.create(
                name=str(fileData), file=fileData, author=req.user, size=fileData.size
            )
            file.save()
            return redirect("/")
        else:
            return redirect("/")
    else:
        return HttpResponse("invalid")


@login_required(login_url="auth/login")
def deleteFile(req, id):
    file = CustomFile.objects.get(id=int(id))
    file.file.delete()
    file.delete()
    return redirect("/")


@login_required(login_url="auth/login")
def createFolder(req):
    return HttpResponse("nope")


@login_required(login_url="auth/login")
def profile(req):
    return render(
        req, template_name="registration/profile.html", context={"user": req.user}
    )


@login_required(login_url="auth/login")
def download_file(req, id):
    file = CustomFile.objects.get(id=int(id))
    file_path = os.path.join("", file.file.path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    raise Http404

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        else:
            print("invalid", form.errors)
            return render(
                request=request,
                template_name="registration/register.html",
                context={"form": form},
            )
    form = NewUserForm()
    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": form},
    )


def create_thumbnail(input_image, thumbnail_size):
    # Load the input image
    # input_image = cv2.imread(input_image_path)

    # Calculate the aspect ratio of the input image
    height, width, channels = input_image.shape
    aspect_ratio = width / height

    # Calculate the size of the thumbnail
    thumbnail_height = int(thumbnail_size / aspect_ratio)
    thumbnail_width = thumbnail_size
    thumbnail_size = (thumbnail_width, thumbnail_height)

    # Resize the input image to create the thumbnail
    thumbnail_image = cv2.resize(input_image, thumbnail_size)

    # Save the thumbnail image to the output path
    return thumbnail_image

    # Example usage
    # create_thumbnail("input_image.jpg", "thumbnail_image.jpg", 100)
