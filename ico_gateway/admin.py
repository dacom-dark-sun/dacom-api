from django.contrib import admin

from ico_gateway.models import IcoProject, IcoWallet

admin.site.register([
    IcoProject,
    IcoWallet
])
